import streamlit as st
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

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
            <p>{post}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Inga inlägg har publicerats ännu.")

# Funktion för att generera PDF och låta användaren ladda ner den
def generate_pdf(posts):
    # Skapa en byte-ström för att hålla PDF:n i minnet
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    width, height = letter

    y_position = height - 40  # Startposition för första inlägget
    padding = 10  # Marginal för text och ram

    # Gå igenom alla inlägg och skapa en PDF för varje inlägg
    for idx, post in enumerate(posts, 1):
        border_color = (0.7, 0.7, 1) if idx % 2 != 0 else (0.7, 1, 0.7)  # RGB för ljusblått och ljusgrönt
        background_color = (224/255, 247/255, 255/255) if idx % 2 != 0 else (232/255, 245/255, 233/255)  # Ljus bakgrund

        # Rita rektangeln för ramen
        c.setStrokeColorRGB(*border_color)  # Ställ in ramfärg
        c.setFillColorRGB(*background_color)  # Ställ in bakgrundsfärg
        c.rect(padding, y_position - 20, width - 2 * padding, 60, fill=1)

        # Lägg till texten för inlägget
        c.setFillColorRGB(0, 0, 0)  # Svart text
        c.drawString(padding + 5, y_position, f"Inlägg {idx}:")
        c.drawString(padding + 5, y_position - 15, post)

        # Justera y-positionen för nästa inlägg
        y_position -= 80  # Öka utrymmet mellan inläggen

        # Om det inte finns tillräckligt med plats för nästa inlägg, skapa en ny sida
        if y_position < 100:
            c.showPage()
            y_position = height - 40

    # Spara PDF:en till byte-strömmen
    c.save()

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
    if password == "dittLösenord123":  # Byt ut detta lösenord mot det önskade
        delete_all_posts()
        save_posts(st.session_state["posts"])  # Spara den tomma listan
        st.success("Alla inlägg har raderats!")
    else:
        st.error("Fel lösenord. Försök igen.")
