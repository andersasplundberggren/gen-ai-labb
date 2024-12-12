import streamlit as st
import os
import json
from io import BytesIO
from PIL import Image

# Fil för att lagra inlägg
POSTS_FILE = "posts.json"

# Funktion för att läsa inlägg från fil
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r") as file:
            return json.load(file)
    return []

# Funktion för att spara inlägg till fil
def save_posts(posts):
    with open(POSTS_FILE, "w") as file:
        json.dump(posts, file)

# Funktion för att radera alla inlägg
def delete_all_posts():
    if os.path.exists(POSTS_FILE):
        os.remove(POSTS_FILE)
    st.session_state["posts"] = []

# Ladda tidigare inlägg
if "posts" not in st.session_state:
    st.session_state["posts"] = load_posts()

# Konfigurera sidan
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

# Sidrubrik
st.markdown("## Skapa och Dela Innehåll")

# Filuppladdning för bild
uploaded_file = st.file_uploader("Ladda upp en bild:", type=["jpg", "jpeg", "png"])

# Publicera och ladda om-knappar
col1, col2 = st.columns(2)
with col1:
    if st.button("Publicera"):
        if uploaded_file is not None:
            # Lägg till bilden i inläggen
            image_data = BytesIO(uploaded_file.read())
            st.session_state["posts"].append(image_data.getvalue())
            save_posts(st.session_state["posts"])  # Spara inlägget till fil
            st.success("Din bild har publicerats!")
            # Omdirigera för att simulera en sidladdning
            st.set_query_params(reload="true")
        else:
            st.warning("Du måste ladda upp en bild för att publicera.")
with col2:
    if st.button("Ladda om sidan"):
        # Omdirigera för att simulera en sidladdning
        st.set_query_params(reload="true")

# Visa alla publicerade inlägg
st.markdown("### Publicerade Inlägg")
if st.session_state["posts"]:
    col1, col2 = st.columns(2)
    for idx, post in enumerate(st.session_state["posts"], 1):
        # Växla färg beroende på index (fyra olika färger)
        if idx % 4 == 1:
            border_color = "lightblue"
            background_color = "#e0f7ff"
        elif idx % 4 == 2:
            border_color = "lightgreen"
            background_color = "#e8f5e9"
        elif idx % 4 == 3:
            border_color = "red"
            background_color = "#ffe0e0"
        else:
            border_color = "yellow"
            background_color = "#ffffe0"

        # Visa bilden i en inläggsruta
        post_html = f"""
        <div style="border: 2px solid {border_color}; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: {background_color};">
            <strong>Inlägg {idx}:</strong><br>
            <img src="data:image/png;base64,{post.decode('utf-8')}" alt="Inlägg {idx}" style="width:100%; max-width:300px; height:auto;">
        </div>
        """
        if idx % 2 != 0:
            col1.markdown(post_html, unsafe_allow_html=True)
        else:
            col2.markdown(post_html, unsafe_allow_html=True)
else:
    st.info("Inga inlägg har publicerats ännu.")

# Flytta bort raderingsfunktionen längst ner
st.markdown("### Radera alla inlägg")
password = st.text_input("Ange lösenord för att radera alla inlägg:", type="password")

# Kontrollera om rätt lösenord har angetts
if st.button("Radera alla inlägg"):
    if password == "radera":  # Byt ut detta lösenord mot det önskade
        delete_all_posts()
        save_posts(st.session_state["posts"])  # Spara den tomma listan
        st.success("Alla inlägg har raderats!")
    else:
        st.error("Fel lösenord. Försök igen.")
