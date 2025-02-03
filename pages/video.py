import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
import os
from uuid import uuid4
from functions.styling import page_config, styling
from functions.menu import menu
import config as c

### CSS AND STYLING
st.logo("images/logome.png", icon_image="images/logo_small.png")
page_config()
styling()

st.title("Chatta med ett förinläst dokument")

# Ensure each session has a unique ID
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid4())

# Path to preloaded documents
document_folder = './data/preloaded_documents'
os.makedirs(document_folder, exist_ok=True)

# Admin settings for uploading new documents
ADMIN_PASSWORD = "admin123"  # Ändra detta till ett säkert lösenord

if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

with st.sidebar:
    st.subheader("Admin")
    if not st.session_state["admin_authenticated"]:
        admin_password = st.text_input("Ange admin-lösenord", type="password")
        if st.button("Logga in"):
            if admin_password == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                st.success("Inloggad som admin!")
            else:
                st.error("Fel lösenord")

    if st.session_state["admin_authenticated"]:
        uploaded_file = st.file_uploader("Ladda upp ett nytt dokument", type=("pdf", "docx", "txt"))
        if uploaded_file:
            file_path = os.path.join(document_folder, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success(f"Filen {uploaded_file.name} har laddats upp!")

# Load preloaded documents
@st.cache_resource(show_spinner=True)
def load_preloaded_data():
    with st.spinner("Laddar det förinlästa dokumentet..."):
        data = SimpleDirectoryReader(input_dir=document_folder, recursive=True).load_data()
        index = VectorStoreIndex.from_documents(
            data,
            llm=Settings.llm,
            embed_model=Settings.embed_model,
            show_progress=True
        )
        return index

index = load_preloaded_data()
query_engine = index.as_query_engine(chat_mode="openai", streaming=True, similarity_top_k=20, verbose=True)

# Chat functionality
if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [{"role": "assistant", "content": "Hej! Hur kan jag hjälpa dig med dokumentet?"}]

if prompt := st.chat_input("Din fråga?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        full_response = ""
        message_placeholder = st.empty()
        with st.spinner("Jag tänker... Ett ögonblick..."):
            streaming_response = query_engine.query(prompt)
            for response in streaming_response.response_gen:
                full_response += response
                message_placeholder.markdown(full_response + "▌")
            message = {"role": "assistant", "content": full_response}
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(message)
