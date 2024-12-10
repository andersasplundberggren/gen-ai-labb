# External imports
import streamlit as st
from llama_index.core.llms import ChatMessage
from openai import OpenAI
from groq import Groq

# Python imports
import hmac
import os
from os import environ

# Local imports 
from functions.styling import page_config, styling
from functions.menu import menu
import config as c

# CSS AND STYLING
st.logo("images/logome.png", icon_image="images/logo_small.png")

page_config()
styling()

# Utfällbar textruta med bilder och punktlista
# with st.expander("### Övning"):
    st.markdown("""
        ### Sammanfatta text och skapa quiz:
        - Gå till Wikipedia och hitta en artikel.
        - Markera och kopiera texten från artikeln.
        - Klistra in texten och skriv en prompt för att be chatbotten summera artikeln.
        - Skriv in prompt där du ber om en quiz med 10 frågor baserat på innehållet i texten.
    """)
    # st.write("Tips. Skriv din prompt gör sedan radbryt med hjälp av shift + enter och skriv in tre --- och efter det ytterligare ett radbryt med shift + enter. Klistra sedan in texten som du kopierat.")

# Check if language is already in session_state, else initialize it with a default value
if 'language' not in st.session_state:
    st.session_state['language'] = "Svenska"  # Default language

st.session_state["pwd_on"] = st.secrets.pwd_on

### PASSWORD
if st.session_state["pwd_on"] == "true":

    def check_password():
        if c.deployment == "streamlit":
            passwd = st.secrets["password"]
        else:
            passwd = environ.get("password")

        def password_entered():
            if hmac.compare_digest(st.session_state["password"], passwd):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        if st.session_state.get("password_correct", False):
            return True

        st.text_input("Lösenord", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state:
            st.error("😕 Ooops. Fel lösenord.")
        return False

    if not check_password():
        st.stop()

# Translation
if st.session_state['language'] == "Svenska":
    chat_prompt = "Du är en hjälpsam AI-assistent. Svara på användarens frågor."
    chat_imput_q = "Vad vill du prata om?"

elif st.session_state['language'] == "English":
    chat_prompt = "You are a helpful AI assistant. Answer the user’s questions."
    chat_imput_q = "What do you want to talk about?"

prompt = f"{chat_prompt}"

if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = prompt

if "llm_temperature" not in st.session_state:
    st.session_state["llm_temperature"] = 0.7
if "llm_chat_model" not in st.session_state:
    st.session_state["llm_chat_model"] = "OpenAI GPT-4o mini"

# SIDEBAR
menu()

st.sidebar.warning("""Det här är en prototyp där information du matar in 
                       bearbetas med en språkmodell. 
                       Prototypen är __inte GDPR-säkrad__, då den använder AI-modeller 
                       som körs på servrar i USA.""")

### MAIN PAGE

# Inledande meddelanden
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

# Ny sektion: Lägga till text och bilder
st.markdown("### Skapa och dela innehåll")

# Text area för textinmatning
user_text = st.text_area(
    label="Skriv in din text här",
    placeholder="Skriv något intressant...",
    height=200
)

# Möjlighet att ladda upp bilder
uploaded_images = st.file_uploader(
    label="Ladda upp bilder",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Visa text och bilder när användaren klickar på "Visa innehåll"
if st.button("Visa innehåll"):
    st.markdown("### Innehåll")
    if user_text:
        st.markdown("#### Text")
        st.markdown(user_text)
    else:
        st.warning("Ingen text inmatad.")

    if uploaded_images:
        st.markdown("#### Bilder")
        for image in uploaded_images:
            st.image(image, caption=image.name)
    else:
        st.warning("Inga bilder uppladdade.")
