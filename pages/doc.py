import streamlit as st
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
    response = openai.Embedding.create(
        model="text-embedding-003", input=text
    )
    embedding = response['data'][0]['embedding']
    data = {"content": text, "embedding": embedding}
    supabase.table("documents").insert(data).execute()

# Funktion för att hämta alla dokument från Supabase och matcha med användarens fråga
def search_documents(query):
    # Hämta alla dokument från Supabase
    documents = supabase.table("documents").select("content", "embedding").execute().data

    # Skapa en embedding för frågan
    query_response = openai.Embedding.create(
        model="text-embedding-003", input=query
    )
    query_embedding = query_response['data'][0]['embedding']
    
    # Funktion för att beräkna likheten mellan två embeddings (kan använda cosine similarity)
    def calculate_similarity(embedding1, embedding2):
        # Beräkna cosine similarity (det här är ett enkelt exempel, men du kan använda en dedikerad metod för det)
        import numpy as np
        return np.dot(np.array(embedding1), np.array(embedding2)) / (np.linalg.norm(np.array(embedding1)) * np.linalg.norm(np.array(embedding2)))
    
    # Hitta matchande dokument baserat på högsta likhet
    results = []
    for doc in documents:
        similarity = calculate_similarity(query_embedding, doc['embedding'])
        if similarity > 0.7:  # Tröskel för att definiera om ett dokument matchar
            results.append(doc)
    
    return results

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
