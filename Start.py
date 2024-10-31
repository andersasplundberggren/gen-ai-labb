# External imports
import streamlit as st

# Python imports
import hmac
import os

# Local imports
import config as c
from functions.styling import page_config, styling
from functions.menu import menu


### CSS AND STYLING

st.logo("images/logo_main.png", icon_image = "images/logo_small.png")

page_config()
styling()

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

### ### ###

st.session_state["app_version"] = c.app_version
st.session_state["update_date"] = c.update_date

### SIDEBAR

menu()

### MAIN PAGE

st.image("images/logo_main.png", width = 400)
st.markdown("###### ")

st.image("images/me.png")
st.markdown("###### ")

st.markdown("""
            __Välkommen till min labbyta för generativ AI__"""
)
st.markdown("""
            Testa att labba under de olika tjnästerna till vänster.
            """)
    
st.markdown("# ")

# External imports
import streamlit as st

# Python imports
import hmac
import os

# Local imports
import config as c
from functions.styling import page_config, styling
from functions.menu import menu


### CSS AND STYLING

st.logo("images/logo_main.png", icon_image="images/logo_small.png")

page_config()
styling()

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
            passwd = os.environ.get("password")

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

### ### ###

st.session_state["app_version"] = c.app_version
st.session_state["update_date"] = c.update_date

### SIDEBAR

menu()

### MAIN PAGE

st.image("images/logo_main.png", width=400)
st.markdown("###### ")

st.image("images/me.png")
st.markdown("###### ")

st.markdown("__Välkommen till min labbyta för generativ AI__")
st.markdown("Testa att labba under de olika tjänsterna till vänster.")

# Define the subpages with titles, descriptions, and image paths
subpages = [
    {
        "title": "Chat",
        "description": "Kort beskrivning av chat.",
        "image": "images/chat.png",  # Byt ut till rätt bildväg
        "link": "https://aspislabb.streamlit.app/chatbot"  # Byt ut till rätt länk
    },
    {
        "title": "Bild",
        "description": "Kort beskrivning av bild.",
        "image": "images/image.png",
        "link": "https://aspislabb.streamlit.app/image"
    },
    {
        "title": "Bildanalys",
        "description": "Kort beskrivning av bildanalys.",
        "image": "images/image.png",
        "link": "https://aspislabb.streamlit.app/image_analysis"
    },
    {
        "title": "Dokumentchat",
        "description": "Kort beskrivning av dokumentchat.",
        "image": "images/description.png",
        "link": "https://aspislabb.streamlit.app/chat_with_document"
    },
    {
        "title": "Transribering",
        "description": "Kort beskrivning av transkribering.",
        "image": "images/transcribe.png",
        "link": "https://aspislabb.streamlit.app/transcribe"
    },
]

# Display the subpages
for page in subpages:
    cols = st.columns([1, 2])  # Förhållande mellan kolumnerna (1:2)
    
    with cols[0]:
        st.image(page['image'], use_column_width=True)  # Bilden till vänster
    
    with cols[1]:
        st.markdown(f"### [{page['title']}]({page['link']})")  # Länk med titel
        st.markdown(page['description'])  # Beskrivning
    
    st.markdown("---")  # Separator mellan undersidor
