import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json

# Initiera Firebase
cred = credentials.Certificate('path/to/your/firebase/credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id.firebaseio.com/'
})

# Filreferens till Firebase Realtime Database
posts_ref = db.reference('posts')

# Funktion för att hämta alla inlägg från Firebase
def load_posts():
    posts = posts_ref.get()
    return posts if posts else []

# Funktion för att spara ett nytt inlägg till Firebase
def save_post(post):
    posts_ref.push(post)

# Ladda tidigare inlägg från Firebase
if "posts" not in st.session_state:
    st.session_state["posts"] = load_posts()

# Sidkonfiguration
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

# Sidrubrik
st.markdown("## Skapa och Dela Innehåll")

# Textområde för att skriva inlägg
user_text = st.text_area(
    label="Skriv ditt inlägg:",
    placeholder="Dela något intressant...",
    height=150
)

# Publicera-knapp
if st.button("Publicera"):
    if user_text.strip():
        # Lägg till nytt inlägg till Firebase
        save_post(user_text.strip())
        st.session_state["posts"].append(user_text.strip())  # Lägg till det till sessionen också
        st.success("Ditt inlägg har publicerats!")
    else:
        st.warning("Inlägget kan inte vara tomt.")

# Visa alla publicerade inlägg
st.markdown("### Publicerade Inlägg")
if st.session_state["posts"]:
    for idx, post in enumerate(st.session_state["posts"], 1):
        st.markdown(f"**Inlägg {idx}:**")
        st.markdown(f"{post}")
else:
    st.info("Inga inlägg har publicerats ännu.")

# Lyssna på förändringar i realtid (du kan använda Firebase’s realtidslyssnare här)
def listen_for_changes():
    posts_ref.listen(lambda event: st.experimental_rerun())

# Starta lyssnaren för förändringar (kan köras i bakgrunden)
listen_for_changes()
