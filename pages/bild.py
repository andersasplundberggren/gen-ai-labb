import streamlit as st
import os
from PIL import Image
from fpdf import FPDF

# Mapp för att spara bilder
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Titel och instruktioner
st.title("Bilddelning med Streamlit")
st.write("Ladda upp en bild så delas den med alla besökare på sidan.")

# Ladda upp bild
uploaded_file = st.file_uploader("Ladda upp en bild", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Spara bilden till servern
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Bilden '{uploaded_file.name}' har laddats upp och är nu delad!")

# Visa alla uppladdade bilder
st.header("Delade bilder")
image_files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]

if image_files:
    cols = st.columns(3)  # Skapa tre kolumner
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(UPLOAD_DIR, image_file)
        image = Image.open(image_path)
        col = cols[idx % 3]  # Välj kolumn baserat på index
        with col:
            st.image(image, caption=image_file, use_container_width=True)
else:
    st.write("Inga bilder har laddats upp ännu.")

# Funktion för att ladda ned alla bilder som en PDF med lösenordsskydd
st.header("Ladda ned alla bilder")
password = st.text_input("Ange lösenord för att ladda ned bilder", type="password")

if st.button("Skapa och ladda ned PDF"):
    if password == "hemligt":  # Ersätt "hemligt" med ditt önskade lösenord
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        for image_file in image_files:
            image_path = os.path.join(UPLOAD_DIR, image_file)
            pdf.add_page()
            pdf.image(image_path, x=10, y=10, w=190)

        pdf_filename = "bilder.pdf"
        pdf.output(pdf_filename)

        with open(pdf_filename, "rb") as f:
            st.download_button(
                label="Ladda ned PDF",
                data=f,
                file_name=pdf_filename,
                mime="application/pdf"
            )
        os.remove(pdf_filename)  # Ta bort PDF-filen efter nedladdning
    else:
        st.error("Fel lösenord! Försök igen.")
