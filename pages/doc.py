import streamlit as st
from uuid import uuid4
import chromadb
from openai.embeddings_utils import get_embedding
from llama_index.llms.openai import OpenAI

# Skapa en ChromaDB-klient
client = chromadb.Client()
collection = client.create_collection("documents")

# Lägg till en funktion för att indexera text
def index_texts(texts, collection):
    for text in texts:
        embedding = get_embedding(text, model="text-embedding-003")
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": "manual"}],
            ids=[str(uuid4())]
        )

# Indexera din text här
texts_to_index = [
    "Text",
    "Här är en annan text som chatten kan använda för att generera svar."
]
index_texts(texts_to_index, collection)

# Sök funktion
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
    for result in results:
        st.write(f"**Resultat:** {result}")
