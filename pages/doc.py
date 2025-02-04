import streamlit as st
from uuid import uuid4
import chromadb
from openai.embeddings_utils import get_embedding
import openai
from supabase import create_client, Client

# Sätt upp OpenAI API-nyckel
openai.api_key = "din-openai-api-nyckel"

# Sätt upp Supabase
SUPABASE_URL = "https://rtswtxendsfmejlxeqcg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0c3d0eGVuZHNmbWVqbHhlcWNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE1MTY0MzcsImV4cCI6MjA0NzA5MjQzN30.EHf-P_JyRTJix7Y6YYWw3KIQ0CIwpbWWCtxfHRihWIw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Skapa en ChromaDB-klient
client = chromadb.Client()
collection = client.create_collection("documents")

# Hämta och indexera text från Supabase
def fetch_and_index_documents(collection):
    response = supabase.table("documents").select("content").execute()
    texts = [doc["content"] for doc in response.data]
    for text in texts:
        embedding = get_embedding(text, model="text-embedding-003")
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": "supabase"}],
            ids=[str(uuid4())]
        )

fetch_and_index_documents(collection)

# Sökfunktion

def search_documents(query, collection):
    query_embedding = get_embedding(query, model="text-embedding-003")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    return results['documents']

# Streamlit-app
st.title("AI Chat med dokument")

query = st.text_input("Ställ din fråga:")

if query:
    results = search_documents(query, collection)
    if results:
        for result in results:
            st.write(f"**Resultat:** {result}")
    else:
        st.write("Inga resultat funna.")
