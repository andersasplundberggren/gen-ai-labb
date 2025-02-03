import streamlit as st
import os
from uuid import uuid4
import shutil

# Skapa en mapp för uppladdade dokument om den inte finns
DOCUMENT_FOLDER = "./data/uploaded_documents"
os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

# Lösenord för admininloggning
ADMIN_PASSWORD = "admin123"  # Ändra lösenordet här

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

# Administratörsinloggning
def admin_login():
    password = st.text_input("Lösenord", type="password")
    if password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.success("Inloggning lyckades!")
    elif password:
        st.error("Fel lösenord. Försök igen.")

# Om användaren är administratör
if 'is_admin' in st.session_state and st.session_state.is_admin:
    st.sidebar.title("Adminpanel")
    action = st.sidebar.radio("Vad vill du göra?", ["Se uppladdade dokument", "Ta bort dokument"])

    if action == "Se uppladdade dokument":
        st.subheader("Uppladdade dokument")
        uploaded_files = os.listdir(DOCUMENT_FOLDER)
        if uploaded_files:
            for file in uploaded_files:
                st.write(file)
        else:
            st.write("Inga dokument har laddats upp än.")
    
    if action == "Ta bort dokument":
        st.subheader("Ta bort ett dokument")
        uploaded_files = os.listdir(DOCUMENT_FOLDER)
        file_to_delete = st.selectbox("Välj dokument att ta bort", uploaded_files)
        if st.button("Ta bort"):
            file_path = os.path.join(DOCUMENT_FOLDER, file_to_delete)
            os.remove(file_path)
            st.success(f"Dokumentet '{file_to_delete}' har tagits bort.")
        else:
            st.write("Välj ett dokument för att ta bort det.")

# Om inte administratör, fortsätt med chatt
else:
    # Om ingen admin är inloggad, visa inloggningsformulär
    if 'is_admin' not in st.session_state:
        admin_login()

    # Ladda upp dokument om ingen finns i sessionen
    if 'uploaded_file' not in st.session_state:
        uploaded_file_path = upload_document()
    else:
        uploaded_file_path = st.session_state.uploaded_file

    # Ladda och indexera dokument om de finns
    if uploaded_file_path:
        # Indexering av uppladdade dokument
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
