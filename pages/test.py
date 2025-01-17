# External imports
import streamlit as st
from fpdf import FPDF
from PIL import Image
import os
import hmac
import config as c
from functions.menu import menu  # Lägg till denna import för att inkludera menyn

# CSS AND STYLING
st.logo("images/logome.png", icon_image="images/logo_small.png")

# Konfigurera sidan
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

# Ny sektion: Skapa och dela innehåll
st.markdown("### Dokumentera")

# Meny - Lägg till den från tidigare kod
menu()

# Text area för textinmatning
user_text = st.text_area(
    label="Här kan du lägga in text som du genererat fram eller en prompt som blev bra.",
    placeholder="Skriv något intressant...",
    height=200
)

# Möjlighet att ladda upp bilder
uploaded_images = st.file_uploader(
    label="Här kan du ladda upp bilder som du genererat fram. Bilderna ihop med texten kan sedan laddas ned som en PDF.",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Visa text och bilder när användaren klickar på "Visa innehåll"
if st.button("Visa innehåll"):
    st.markdown("### Innehåll")
    if user_text:
        st.markdown("#### Text")
        st.markdown(user_text)
    else:
        st.warning("Ingen text inmatad.")

    if uploaded_images:
        st.markdown("#### Bilder")
        for image in uploaded_images:
            st.image(image, caption=image.name)
    else:
        st.warning("Inga bilder uppladdade.")

# Funktion för att skapa PDF
def generate_pdf(text, images):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Lägg till text
    if text:
        pdf.multi_cell(0, 10, text)
        pdf.ln(10)

    # Lägg till bilder
    for img in images:
        image = Image.open(img)
        image_path = f"temp_{img.name}"
        image.save(image_path)
        pdf.image(image_path, x=10, y=None, w=190)  # Anpassa bredden till PDF-sidans bredd
        os.remove(image_path)  # Radera tillfällig bildfil

    return pdf


# Ladda ned PDF
if st.button("Ladda ned som PDF"):
    if not user_text and not uploaded_images:
        st.warning("Ingen text eller bild att ladda ned.")
    else:
        # Generera PDF
        pdf = generate_pdf(user_text, uploaded_images)

        # Spara till en temporär fil
        pdf_path = "content.pdf"
        pdf.output(pdf_path)

        # Gör filen tillgänglig för nedladdning
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="📥 Ladda ned PDF",
                data=file,
                file_name="innehåll.pdf",
                mime="application/pdf"
            )

        # Ta bort temporär fil
        os.remove(pdf_path)

