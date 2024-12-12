import streamlit as st
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

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

# Skapa en meny för att växla mellan undersidor
page = st.selectbox("Välj sida", ["Skapa Inlägg", "Publicerade Inlägg och PDF Export"])

if page == "Skapa Inlägg":
    # Sidrubrik
    st.markdown("## Skapa och Dela Innehåll")

    # Textområde för textinmatning
    user_text = st.text_area(
        label="Skriv ditt inlägg:",
        placeholder="Dela något intressant...",
        height=150
    )

    # Publicera-knapp
    if st.button("Publicera"):
        if user_text.strip():
            st.session_state["posts"].append(user_text.strip())
            save_posts(st.session_state["posts"])  # Spara inlägget till fil
            st.success("Ditt inlägg har publicerats!")
        else:
            st.warning("Inlägget kan inte vara tomt.")

elif page == "Publicerade Inlägg och PDF Export":
    # Sidrubrik
    st.markdown("## Publicerade Inlägg")

    # Visa alla publicerade inlägg
    if st.session_state["posts"]:
        for idx, post in enumerate(st.session_state["posts"], 1):
            st.markdown(f"**Inlägg {idx}:** {post}")
    else:
        st.info("Inga inlägg har publicerats ännu.")

    # Funktion för att generera PDF och låta användaren ladda ner den
    def generate_pdf(posts):
        # Skapa en byte-ström för att hålla PDF:n i minnet
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

        # Skapa stil
        styles = getSampleStyleSheet()
        style_normal = styles["Normal"]

        # Förbered texten
        story = []
        for idx, post in enumerate(posts, 1):
            post_text = f"Inlägg {idx}:\n{post}"
            paragraph = Paragraph(post_text, style_normal)
            story.append(paragraph)
            story.append(Spacer(1, 12))  # Lägg till lite mellanrum mellan inlägg

            # Lägg till sidbrytning efter varje inlägg
            doc.showPage()

        # Skapa PDF
        doc.build(story)

        # Gå tillbaka till början av byte-strömmen
        buffer.seek(0)

        return buffer

    # Ladda ner PDF-knapp
    if st.button("Ladda ner alla inlägg som PDF"):
        if st.session_state["posts"]:
            pdf_buffer = generate_pdf(st.session_state["posts"])
            st.download_button(
                label="Ladda ner PDF",
                data=pdf_buffer,
                file_name="inlägg.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Det finns inga inlägg att ladda ner.")

    # Radera alla inlägg
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
