# External imports
import streamlit as st
from openai import OpenAI

# Python imports
import hmac
from PIL import Image
import os
from os import environ

# Local imports
from functions.styling import page_config, styling
import config as c
from functions.menu import menu

### CSS AND STYLING

st.logo("images/logome.png", icon_image="images/logo_small.png")

page_config()
styling()

# Utfällbar textruta med bilder och punktlista
with st.expander("### Övning"):  # Gör rubriken lika stor som underrubriken
    st.markdown("""
        ### Testa att generera bilderna:
        Här bör vi tänka BIAS och vilken träningsdata som nyttjas när bilderna ska genereras. Det finns risk för att du inte alls får de bilder du är på jakt efter.

        - En mörkhyad doktor som behandlar vita fattiga barn
        - En brud som bär sin brudgum över tröskeln
        - En skäggig kvinna
        - En kvinnlig bilmekaniker
        - En framgångsrik chef/ledare
    """)

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

### ### ### ###

# Translation

if st.session_state['language'] == "Svenska":
    image_describe = "Beskriv din bild..."
    image_clear_chat = "Rensa chat"
    image_hello = "Hej! Hur kan jag hjälpa dig?"
    image_settings = "Inställningar"
    image_choose_model = "Välj modell"
    image_choose_size = "Välj bildstorlek"
    image_wait = "Ett ögonblick... Ritar och färglägger din bild..."
    image_sidebar = "Det finns inget minne i chatten, du måste beskriva din bild varje gång."

elif st.session_state['language'] == "English":
    image_describe = "Describe your image..."
    image_clear_chat = "Clear chat"
    image_hello = "Hi! How can I help you?"
    image_settings = "Settings"
    image_choose_model = "Choose model"
    image_choose_size = "Choose image size"
    image_wait = "One moment… Drawing and coloring your image…"
    image_sidebar = "Det finns inget minne i chatten, utan du måste beskriva din bild varje gång."

if c.deployment == "streamlit":
    client = OpenAI(api_key=st.secrets.openai_key)
else:
    client = OpenAI(api_key=environ.get("openai_key"))

### SIDEBAR

menu()

st.sidebar.success(f"{image_sidebar}")

st.sidebar.warning("""Det här är en prototyp där information du matar in 
                       bearbetas med en språkmodell. 
                       Prototypen är __inte GDPR-säkrad__, då den använder AI-modeller 
                       som körs på servrar i USA.""")

# Initiera standardvärden i session_state
if "image_size" not in st.session_state:
    st.session_state["image_size"] = "1024x1024"
if "image_model" not in st.session_state:
    st.session_state["image_model"] = "dall-e-3"

col1, col2 = st.columns(2)

with col1:
    if st.button(f"{image_clear_chat}", type="secondary"):
        if "messages" in st.session_state.keys():  # Initialize the chat message history
            st.session_state.messages = [
                {"role": "assistant", "content": f"{image_hello}"}
            ]

with col2:
    with st.expander(f"{image_settings}"):
        image_model = st.selectbox(f"{image_choose_model}", ["Dall-E 3"])
        image_size = st.selectbox(f"{image_choose_size}", ["1024x1024", "1792x1024"], index=0)

        st.session_state["image_model"] = "dall-e-3"  # Endast Dall-E 3 stöds i detta exempel
        st.session_state["image_size"] = image_size

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"{image_hello}"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"].startswith("http"):  # Check if the content is an image URL
            st.image(message["content"])
        else:
            st.markdown(message["content"])

if prompt := st.chat_input(f"{image_describe}"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"{image_wait}"):
            response = client.images.generate(
                model=st.session_state["image_model"],
                prompt=prompt,
                size=st.session_state["image_size"],
                style="vivid",
                n=1,
            )

            # Store the image URL
            image_url = response.data[0].url

            # Display the image immediately
            st.image(image_url, caption=prompt)

        # Append the image URL to the messages
        st.session_state.messages.append({"role": "assistant", "content": image_url})
