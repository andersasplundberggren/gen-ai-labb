import streamlit as st
import os
from PIL import Image
from fpdf import FPDF
import base64

# Mapp för att spara bilder
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Funktion för att konvertera bild till base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Titel och instruktioner
st.title("Bilddelning")
st.write("Ladda upp en bild.")

# Ladda upp bild (tillåter alla användare utan inloggning)
uploaded_file = st.file_uploader("Ladda upp en bild", type=["png", "jpg", "jpeg"], key="file_uploader_1")

if uploaded_file is not None:
    # Spara bilden till servern
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Bilden '{uploaded_file.name}' har laddats upp och är nu delad!")

# Funktion för att skapa en helskärmseffekt för bilden
def open_fullscreen_image(img_base64, image_file):
    return f"""
    <div class="image-container">
        <img src="data:image/png;base64,{img_base64}" alt="{image_file}" style="cursor: pointer; width: 100%; border-radius: 8px;" onclick="openImage(this)">
    </div>

    <script>
        function openImage(imgElement) {{
            const imgSrc = imgElement.src;
            const imgWindow = window.open("", "_blank");
            imgWindow.document.write('<img src="' + imgSrc + '" style="width: 100%; height: 100%; object-fit: contain;">');
        }}
    </script>
    """

# Visa alla uppladdade bilder med skugga och helskärmseffekt
st.header("Delade bilder")
image_files = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]

if image_files:
    cols = st.columns(3)  # Skapa tre kolumner
    for idx, image_file in enumerate(image_files):
        image_path = os.path.join(UPLOAD_DIR, image_file)
        image = Image.open(image_path)
        # Konvertera bild till base64
        img_base64 = img_to_base64(image_path)
        col = cols[idx % 3]  # Välj kolumn baserat på index
        with col:
            # Lägg till skugga och helskärmseffekt med hjälp av CSS och JavaScript
            st.markdown(
                f"""
                <div style="box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 8px;">
                    {open_fullscreen_image(img_base64, image_file)}
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.write("Inga bilder har laddats upp ännu.")

# Administratörsinloggning (diskret och smalare högst upp på sidan)
admin_password = None
login_expanded = st.empty()  # Behåll en tom plats för inloggning

# Skapa ett diskret och smalare inloggningsfält för administratören
with login_expanded.container():
    col1, col2, col3 = st.columns([1, 6, 1])  # Skapa tre kolumner för att centrera inputfältet
    with col2:
        admin_password = st.text_input("Admin-lösenord", type="password", placeholder="Lösenord", key="admin")

# Kontrollera om lösenordet är rätt
if admin_password == "admin123":  # Byt ut "admin123" mot ditt önskade lösenord
    st.success("Du är inloggad som administratör!")

    # Ladda upp bild (tillåter alla användare)
    uploaded_file = st.file_uploader("Ladda upp en bild", type=["png", "jpg", "jpeg"], key="file_uploader_2")

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
            # Konvertera bild till base64
            img_base64 = img_to_base64(image_path)
            col = cols[idx % 3]  # Välj kolumn baserat på index
            with col:
                # Lägg till skugga och helskärmseffekt med hjälp av CSS och JavaScript
                st.markdown(
                    f"""
                    <div style="box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 8px;">
                        {open_fullscreen_image(img_base64, image_file)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.write("Inga bilder har laddats upp ännu.")

    # Ladda ned alla bilder som PDF
    if st.button("Skapa och ladda ned PDF"):
        if image_files:
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
            os.remove(pdf_filename)
        else:
            st.warning("Inga bilder att inkludera i PDF:en.")

    # Radera alla bilder
    if st.button("Radera alla bilder"):
        if image_files:
            for image_file in image_files:
                os.remove(os.path.join(UPLOAD_DIR, image_file))
            st.success("Alla bilder har raderats.")
        else:
            st.warning("Det finns inga bilder att radera.")
else:
    if admin_password:
        st.warning("Fel lösenord eller ingen åtkomst till administratörsdel.")
