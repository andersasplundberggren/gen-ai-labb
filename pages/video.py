import streamlit as st
import os
from uuid import uuid4
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Skapa en mapp för uppladdade dokument om den inte finns
DOCUMENT_FOLDER = "./data/uploaded_documents"
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

# Funktion för att ladda upp dokument
def upload_document():
    uploaded_file = st.file_uploader("Ladda upp ett dokument", type=["pdf", "txt", "docx", "csv"])
    if uploaded_file is not None:
        # Generera unikt filnamn för att undvika namnkonflikter
        unique_filename = f"{uuid4().hex}_{uploaded_file.name}"
        file_path = os.path.join(DOCUMENT_FOLDER, unique_filename)
        
        # Spara filen lokalt på servern
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Lagra filnamnet i session_state så att det finns kvar under sessionen
        st.session_state.uploaded_file = file_path
        st.success(f"Filen '{uploaded_file.name}' har laddats upp och sparats.")
        
        return file_path
    return None

# Ladda upp dokument om ingen finns i sessionen
if 'uploaded_file' not in st.session_state:
    uploaded_file_path = upload_document()
else:
    uploaded_file_path = st.session_state.uploaded_file

# Ladda och indexera dokument om de finns
@st.cache_resource(show_spinner=True)
def load_preloaded_data():
    with st.spinner("Laddar och indexerar dokument..."):
        data = SimpleDirectoryReader(input_dir=DOCUMENT_FOLDER, recursive=True).load_data()
        index = VectorStoreIndex.from_documents(
            data,
            llm=OpenAI(),
            embed_model=OpenAIEmbedding(),
            show_progress=True
        )
        return index

if uploaded_file_path:
    index = load_preloaded_data()
    query_engine = index.as_query_engine(chat_mode="openai", streaming=True, similarity_top_k=5, verbose=True)

    # Chat-funktionalitet
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hej! Hur kan jag hjälpa dig med dokumentet?"}]

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

else:
    st.warning("Vänligen ladda upp ett dokument för att börja chatta med AI.")
