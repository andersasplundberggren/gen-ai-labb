import streamlit as st
import os
from PIL import Image

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
    for image_file in image_files:
        image_path = os.path.join(UPLOAD_DIR, image_file)
        image = Image.open(image_path)
        st.image(image, caption=image_file, use_container_width=True)
else:
    st.write("Inga bilder har laddats upp ännu.")
