import streamlit as st
from uuid import uuid4
from openai.embeddings_utils import get_embedding
import openai
from supabase import create_client, Client

# Sätt upp OpenAI API-nyckel
openai.api_key = "din-openai-api-nyckel"

# Sätt upp Supabase
SUPABASE_URL = "https://rtswtxendsfmejlxeqcg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0c3d0eGVuZHNmbWVqbHhlcWNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE1MTY0MzcsImV4cCI6MjA0NzA5MjQzN30.EHf-P_JyRTJix7Y6YYWw3KIQ0CIwpbWWCtxfHRihWIw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funktion för att spara text + embedding i Supabase
def save_text_document(doc_name, text):
    embedding = get_embedding(text, model="text-embedding-003")
    data = {"content": text, "embedding": embedding}
    supabase.table("documents").insert(data).execute()

# Funktion för att söka i dokument med embeddings
def search_documents(query):
    query_embedding = get_embedding(query, model="text-embedding-003")
    response = supabase.rpc("match_documents", {"query_embedding": query_embedding}).execute()
    return response.data

# Streamlit UI
st.title("AI Chat med dokument")

st.subheader("Lägg till nytt dokument")
doc_name = st.text_input("Dokumentnamn")
text = st.text_area("Textinnehåll")

if st.button("Spara dokument"):
    save_text_document(doc_name, text)
    st.success(f"Dokument '{doc_name}' sparat!")

st.subheader("Sök i dokument")
query = st.text_input("Ställ din fråga:")
if query:
    results = search_documents(query)
    if results:
        for result in results:
            st.write(f"**Resultat:** {result['content']}")
    else:
        st.write("Inga resultat funna.")
