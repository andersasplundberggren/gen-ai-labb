import streamlit as st
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    st.session_state["post_colors"] = {}

# Ladda tidigare inlägg
if "posts" not in st.session_state:
    st.session_state["posts"] = load_posts()
if "post_colors" not in st.session_state:
    st.session_state["post_colors"] = {}

# Lägg till status för upplåsning
if "unlocked" not in st.session_state:
    st.session_state["unlocked"] = False

# Konfigurera sidan
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

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
        save_posts(st.session_state["posts"])
        st.success("Ditt inlägg har publicerats!")
    else:
        st.warning("Inlägget kan inte vara tomt.")

# Lås upp publicerade inlägg
st.markdown("### Lås upp inlägg")
password = st.text_input("Ange lösenord för att visa publicerade inlägg:", type="password")
if st.button("Lås upp"):
    if password == "lösenord123":
        st.session_state["unlocked"] = True
        st.success("Inläggen har låsts upp!")
    else:
        st.error("Fel lösenord. Försök igen.")

# Visa alla publicerade inlägg i tre kolumner om de är upplåsta
if st.session_state["unlocked"]:
    st.markdown("### Publicerade Inlägg")
    if st.session_state["posts"]:
        # Dela upp layouten i tre kolumner
        columns = st.columns(3)
        for idx, post in enumerate(st.session_state["posts"]):
            # Bestäm vilken kolumn som inlägget ska vara i
            col = columns[idx % 3]

            if idx not in st.session_state["post_colors"]:
                st.session_state["post_colors"][idx] = "white"

            # Klickbar funktionalitet för varje inlägg
            if col.button(f"Inlägg {idx + 1}", key=f"btn{idx}"):
                if st.session_state["post_colors"][idx] == "white":
                    st.session_state["post_colors"][idx] = "#d3d3d3"  # Grå bakgrund
                else:
                    st.session_state["post_colors"][idx] = "white"  # Ursprunglig färg

            # Visa inlägg med aktuell bakgrundsfärg i rätt kolumn
            col.markdown(
                f"""
                <div style="background-color: {st.session_state['post_colors'][idx]}; \
                            padding: 10px; margin-bottom: 10px; border-radius: 5px; \
                            border: 1px solid black;">
                    <p>{post}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Inga inlägg har publicerats ännu.")
else:
    st.warning("Inläggen är låsta. Ange lösenord för att låsa upp dem.")

# Funktion för att generera PDF och låta användaren ladda ner den
def generate_pdf(posts):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    story = []
    for idx, post in enumerate(posts, 1):
        paragraph = Paragraph(f"Inlägg {idx}:\n{post}", style_normal)
        story.append(paragraph)
        story.append(Spacer(1, 12))

    doc.build(story)
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

# Flytta bort raderingsfunktionen längst ner
st.markdown("### Radera alla inlägg")
password = st.text_input("Ange lösenord för att radera alla inlägg:", type="password")

if st.button("Radera alla inlägg"):
    if password == "radera":
        delete_all_posts()
        save_posts(st.session_state["posts"])
        st.success("Alla inlägg har raderats!")
    else:
        st.error("Fel lösenord. Försök igen.")
