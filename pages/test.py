
# Python imports
import os
from os import environ
from datetime import datetime
import hashlib
import hmac
from concurrent.futures import ThreadPoolExecutor
pip install fpdf


# External imports
import streamlit as st
from openai import OpenAI
from audiorecorder import audiorecorder
import tiktoken

# Local imports
from functions.transcribe import transcribe_with_whisper_openai
import config as c
from functions.split_audio import split_audio_to_chunks
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

############

import streamlit as st
from fpdf import FPDF  # Installera fpdf med pip install fpdf

def create_pdf(text):
    """Create a PDF file from the text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    
    # Spara PDF till en fil
    pdf_file_name = "anteckningar.pdf"
    pdf.output(pdf_file_name)
    return pdf_file_name

def main():
    # Andra delar av din kod...

    # Anteckningsfält
    st.markdown("### Gör dina anteckningar")
    if 'notes' not in st.session_state:
        st.session_state['notes'] = ""  # Initiera anteckningar

    # Fritextfält för anteckningar
    notes = st.text_area("Skriv dina anteckningar här:", value=st.session_state['notes'], height=300)

    # Spara anteckningarna i session state
    st.session_state['notes'] = notes

    # Ladda ner PDF
    if st.button("Ladda ner som PDF"):
        pdf_file = create_pdf(st.session_state['notes'])
        st.success("PDF skapad! Ladda ner den nedan.")
        st.download_button("Ladda ner PDF", pdf_file, file_name="anteckningar.pdf")

    # Andra delar av din kod...

if __name__ == "__main__":
    main()
