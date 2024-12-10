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
with st.expander("### Övning"):
    st.markdown("""
        ### Sammanfatta text och skapa quiz:
        - Gå till Wikipedia och hitta en artikel.
        - Markera och kopiera texten från artikeln.
        - Klistra in texten och skriv en prompt för att be chatbotten summera artikeln.
        - Skriv in prompt där du ber om en quiz med 10 frågor baserat på innehållet i texten.
    """)
    st.write("Tips. Skriv din prompt gör sedan radbryt med hjälp av shift + enter och skriv in tre --- och efter det ytterligare ett radbryt med shift + enter. Klistra sedan in texten som du kopierat.")

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
    chat_clear_chat = "Rensa chat"
    chat_hello = "Hej! Hur kan jag hjälpa dig?"
    chat_settings = "Inställningar"
    chat_choose_llm = "Välj språkmodell"
    chat_choose_temp = "Temperatur"
    chat_system_prompt = "Systemprompt"
    chat_save = "Spara"
    chat_imput_q = "Vad vill du prata om?"

elif st.session_state['language'] == "English":
    chat_prompt = "You are a helpful AI assistant. Answer the user’s questions."
    chat_clear_chat = "Clear chat"
    chat_hello = "Hi! How can I help you?"
    chat_settings = "Settings"
    chat_choose_llm = "Choose language model"
    chat_choose_temp = "Temperature"
    chat_system_prompt = "System prompt"
    chat_save = "Save"
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

col1, col2 = st.columns(2)

with col1:
    if st.button(f"{chat_clear_chat}", type="secondary"):
        if "messages" in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": f"{chat_hello}"}
            ]

with col2:
    with st.expander(f"{chat_settings}"):
        llm_model = st.selectbox(
            f"{chat_choose_llm}", 
            ["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"],
            index=["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"].index(st.session_state["llm_chat_model"]),
        )

        llm_temp = st.slider(
            f"{chat_choose_temp}",
            min_value=0.0,
            max_value=1.0,
            step=0.1,
            value=st.session_state["llm_temperature"],
        )

        st.session_state["llm_chat_model"] = llm_model
        st.session_state["llm_temperature"] = llm_temp
        
        model_map = {
            "OpenAI GPT-4o": "gpt-4o",
            "OpenAI GPT-4o mini": "gpt-4o-mini",
            "OpenAI o1-preview": "o1-preview", 
            "OpenAI o1-mini": "o1-mini"
        }

        with st.form("my_form"):
            prompt_input = st.text_area(f"{chat_system_prompt}", prompt, height=200)
            st.session_state.system_prompt = prompt_input   
            st.form_submit_button(f"{chat_save}")

if "OpenAI" in st.session_state["llm_chat_model"]:
    st.sidebar.success("Språkmodell: " + llm_model)
else:
    st.sidebar.success("Språkmodell: " + llm_model)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"{chat_hello}"}]

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
