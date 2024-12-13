import streamlit as st
import os
import json
import random
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

# Färger som kan användas
colors_list = ['yellow', 'green', 'red', 'blue']

# Funktion för att generera en mörkare och ljusare nyans av en färg
def get_shades_of_color(color):
    if color == 'yellow':
        return '#FFF176', '#FFEB3B'  # Ljusgul och mörkgul
    elif color == 'green':
        return '#A5D6A7', '#66BB6A'  # Ljusgrön och mörkgrön
    elif color == 'red':
        return '#FFAB91', '#FF7043'  # Ljusröd och mörkröd
    elif color == 'blue':
        return '#81D4FA', '#64B5F6'  # Ljusblå och mörkblå

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

# Visa alla publicerade inlägg i tre kolumner
st.markdown("### Publicerade Inlägg")
if st.session_state["posts"]:
    # Dela upp layouten i tre kolumner
    columns = st.columns(3)
    for idx, post in enumerate(st.session_state["posts"]):
        # Slumpa en färg för varje inlägg
        random_color = random.choice(colors_list)
        light_color, dark_color = get_shades_of_color(random_color)

        # Bestäm vilken kolumn som inlägget ska vara i
        col = columns[idx % 3]

        # Klickbar funktionalitet för varje inlägg
        if col.button(f"Inlägg {idx + 1}", key=f"btn{idx}"):
            if st.session_state["post_colors"].get(idx) == light_color:
                st.session_state["post_colors"][idx] = "#d3d3d3"  # Grå bakgrund
            else:
                st.session_state["post_colors"][idx] = light_color  # Ursprungsfärg

        # Färg på inlägget baserat på om det har blivit klickat
        current_color = st.session_state["post_colors"].get(idx, light_color)

        # Visa inlägg med aktuell bakgrundsfärg i rätt kolumn
        col.markdown(
            f"""
            <div style="background-color: {current_color}; \
                        border: 2px solid {dark_color}; \
                        padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                <strong>Inlägg {idx + 1}:</strong>
                <p>{post}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("Inga inlägg har publicerats ännu.")

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
