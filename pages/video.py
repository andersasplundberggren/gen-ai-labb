import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
import os
import gdown
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

# Google Drive settings
GOOGLE_DRIVE_FOLDER_ID = https://drive.google.com/drive/folders/1OKSqwyk9JaaYx_MrcZLk-et_KtcMZLd_?usp=drive_link
DOCUMENT_FOLDER = "./data/preloaded_documents"
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

def download_files_from_drive():
    drive_url = f"https://drive.google.com/drive/folders/{GOOGLE_DRIVE_FOLDER_ID}"
    st.info(f"Hämtar filer från {drive_url}")
    # Här kan du implementera en funktion för att ladda ner filer via Google Drive API
    # För enkelhet kan du manuellt spara dokumenten i en offentlig Drive-mapp och ange länkar här.

# Ladda ner dokument vid start
download_files_from_drive()

# Load preloaded documents
@st.cache_resource(show_spinner=True)
def load_preloaded_data():
    with st.spinner("Laddar det förinlästa dokumentet..."):
        data = SimpleDirectoryReader(input_dir=DOCUMENT_FOLDER, recursive=True).load_data()
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
