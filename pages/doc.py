import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from llama_index.core import PromptTemplate
from openai import OpenAI
import os

# Konfiguration
OPENAI_API_KEY = st.secrets["openai_key"]
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")
embed_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY)

# Funktion för att lägga till text i databasen
def add_text_to_db(text, doc_id):
    embedding = embed_fn([text])[0]
    collection.add(documents=[text], ids=[doc_id], embeddings=[embedding])
    st.success("Text har lagts till i databasen!")

# Funktion för att hämta relevanta dokument
def query_db(query):
    embedding = embed_fn([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=3)
    return results["documents"][0] if results["documents"] else []

# Streamlit-gränssnitt
st.title("AI-Chatt baserad på dokument")

# Textinmatning för att lägga till data
with st.expander("Lägg till text i databasen"):
    input_text = st.text_area("Skriv eller klistra in text:")
    doc_id = st.text_input("Ange ett unikt ID för texten:")
    if st.button("Lägg till i databas"):
        if input_text and doc_id:
            add_text_to_db(input_text, doc_id)
        else:
            st.error("Fyll i både text och ett unikt ID!")

# AI-chatt
st.header("Chatta med dina dokument")
user_input = st.text_input("Ställ en fråga:")
if user_input:
    relevant_texts = query_db(user_input)
    if relevant_texts:
        context = "\n".join(relevant_texts)
        prompt = f"Du är en AI-assistent. Använd följande kontext för att besvara frågan:\n{context}\n\nFråga: {user_input}\nSvar:"
        response = OpenAI(api_key=OPENAI_API_KEY).chat.completions.create(
            model="gpt-4o", messages=[{"role": "system", "content": prompt}]
        )
        st.write(response.choices[0].message.content)
    else:
        st.write("Ingen relevant information hittades i databasen.")
