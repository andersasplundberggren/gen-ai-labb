import streamlit as st
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from PIL import Image

# Fil för att lagra inlägg
POSTS_FILE = "posts.json"
IMAGE_FOLDER = "uploaded_images"  # Mapp för att lagra uppladdade bilder

# Skapa mappen för bilder om den inte finns
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

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

# Textområde för textinmatning
user_text = st.text_area(
    label="Skriv ditt inlägg:",
    placeholder="Dela något intressant...",
    height=150
)

# Bilduppladdning
uploaded_image = st.file_uploader("Ladda upp en bild", type=["jpg", "jpeg", "png"])

# Publicera-knapp
if st.button("Publicera"):
    if user_text.strip() or uploaded_image:
        # Spara text och bild i listan
        if uploaded_image:
            # Skapa unikt filnamn för bilden
            image_filename = os.path.join(IMAGE_FOLDER, uploaded_image.name)
            
            # Spara bilden i mappen
            with open(image_filename, "wb") as f:
                f.write(uploaded_image.getbuffer())
            
            st.session_state["posts"].append({"text": user_text.strip(), "image": image_filename})
        else:
            st.session_state["posts"].append({"text": user_text.strip(), "image": None})
        
        save_posts(st.session_state["posts"])  # Spara inlägget till fil
        st.success("Ditt inlägg har publicerats!")
    else:
        st.warning("Inlägget kan inte vara tomt.")

# Visa alla publicerade inlägg
st.markdown("### Publicerade Inlägg")
if st.session_state["posts"]:
    for idx, post in enumerate(st.session_state["posts"], 1):
        # Växla färg beroende på index (varannat inlägg)
        border_color = "lightblue" if idx % 2 != 0 else "lightgreen"
        background_color = "#e0f7ff" if idx % 2 != 0 else "#e8f5e9"  # Ljusare bakgrundsfärger
        
        # Lägg till CSS för att skapa en färgad ram och bakgrund
        st.markdown(f"""
        <div style="border: 2px solid {border_color}; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: {background_color};">
            <strong>Inlägg {idx}:</strong>
            <p>{post['text']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Om det finns en bild, visa den också
        if post["image"]:
            st.image(post["image"], width=300)

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
        # Växla färg beroende på index (varannat inlägg)
        background_color = (224/255, 247/255, 255/255) if idx % 2 != 0 else (232/255, 245/255, 233/255)
        
        # Skapa varje inlägg som ett stycke med radbrytning
        post_text = f"Inlägg {idx}:\n{post['text']}"
        paragraph = Paragraph(post_text, style_normal)
        
        # Lägg till bakgrundsfärgen för inlägget genom att skapa en ram
        story.append(paragraph)
        
        # Lägg till bilden i PDF (om den finns)
        if post["image"]:
            img = Image.open(post["image"])
            story.append(Spacer(1, 12))  # Lite mellanrum före bilden
            story.append(img)
        
        story.append(Spacer(1, 12))  # Lägg till lite mellanrum mellan inlägg

    # Skapa PDF med en färgad bakgrund för varje inlägg
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
