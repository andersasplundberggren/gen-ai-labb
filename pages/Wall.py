import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

# Globala variabler för att lagra inlägg (för tillfällig lagring)
if "posts" not in st.session_state:
    st.session_state["posts"] = []

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

# Möjlighet att ladda upp bilder
uploaded_images = st.file_uploader(
    label="Ladda upp bilder som du vill dela:",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Visa bilder om de laddas upp
if uploaded_images:
    st.markdown("### Uppladdade Bilder")
    for image in uploaded_images:
        st.image(image, caption=image.name)

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
    if not st.session_state["posts"] and not uploaded_images:
        st.warning("Ingen text eller bild att ladda ned.")
    else:
        # Generera PDF
        all_text = "\n\n".join(st.session_state["posts"])
        pdf = generate_pdf(all_text, uploaded_images)

        # Spara till en temporär fil
        pdf_path = "content.pdf"
        pdf.output(pdf_path)

        # Gör filen tillgänglig för nedladdning
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="\ud83d\udcc5 Ladda ned PDF",
                data=file,
                file_name="innehåll.pdf",
                mime="application/pdf"
            )

        # Ta bort temporär fil
        os.remove(pdf_path)
