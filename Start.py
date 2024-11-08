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

st.logo("images/logome.png", icon_image = "images/logo_small.png")

### PAGE CONFIGURATION ###

page_config()  # Flytta page_config() högst upp för att undvika felet
styling()

### CSS AND STYLING

#st.image("images/logome.png", width=400)  # Logga högst upp

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
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Ooops. Fel lösenord.")
        return False

    if not check_password():
        st.stop()

st.session_state["app_version"] = c.app_version
st.session_state["update_date"] = c.update_date

### SIDEBAR

menu()

### MAIN PAGE

st.image("images/logome.png", width=200)
st.markdown("###### ")

# Nytt innehåll med huvudrubrik, underrubriker och punktlistor
st.header("Välkommen till AILABBET")
st.write("Här kan du testa olika tjänster inom AI. Inget av det du gör här sparas så om du får fram en bra text eller snygg bild får du se till att spara den.")

st.markdown("###### ")
st.write("Här nedanför finns lite information som kan vara bra att ha koll på innan du kör igång.")

# Första underrubriken
st.subheader("Vad är Prompt?")
st.write("Kort beskrivning vad prompt är.")
st.markdown("""
    
   - <a href="https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link" target="_blank">Här kan du ladda ned promptguiden</a>  
   - <a href="https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link" target="_blank">Här kan du ladda ned promptbiblioteket</a>  
""", unsafe_allow_html=True)

# Andra underrubriken
st.subheader("Underrubrik 2")
st.write("Här är lite information under den andra underrubriken.")
st.markdown("""
- Punkt 1 under Underrubrik 2
- Punkt 2 under Underrubrik 2
- Punkt 3 under Underrubrik 2
""")

# Tredje underrubriken
st.subheader("Underrubrik 3")
st.write("Här är lite information under den tredje underrubriken.")
st.markdown("""
- Punkt 1 under Underrubrik 3
- Punkt 2 under Underrubrik 3
- Punkt 3 under Underrubrik 3
""")

# Introduktionstexten flyttad till slutet av sidan
st.markdown("###### ")
st.markdown("""
    
    
    <a href="https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link" target="_blank">Här kan du ladda ned promptguiden</a>  
    <a href="https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link" target="_blank">Här kan du ladda ned promptbiblioteket</a>  
""", unsafe_allow_html=True)
