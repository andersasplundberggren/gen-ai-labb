
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

st.image("images/logome.png", width = 400)
st.markdown("###### ")

#st.image("images/me.png")
#st.markdown("###### ")

st.markdown("""
    __Välkommen till min labbyta för generativ AI__
    
    På den här sidan hittar du verktyg för att labba med generativ AI.
    
    <a href="https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link" target="_blank">Här kan du ladda ned promptguiden</a>
""", unsafe_allow_html=True)
<a href="https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link" target="_blank">Här kan du ladda ned promptbiblioteket</a>
""", unsafe_allow_html=True)



st.markdown("# ")
