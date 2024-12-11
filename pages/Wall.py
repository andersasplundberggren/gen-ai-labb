import streamlit as st
from fpdf import FPDF
import os
import json

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

# Ladda tidigare inlägg
if "posts" not in st.session_state:
    st.session_state["posts"] = load_posts()

# Konfigurera sidan
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

# Automatisk uppdatering med JavaScript
st.markdown(
    """
    <script>
    setTimeout(function(){
        window.location.reload();
    }, 5000);
    </script>
    """,
    unsafe_allow_html=True,
)

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
        st.markdown(f"**Inlägg {idx}:**")
        st.markdown(f"{post}")
else:
    st.info("Inga inlägg har publicerats ännu.")

# Funktion för att skapa PDF med Unicode-stöd
class PDFWithUnicode(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
        self.set_font('DejaVu', size=12)

    def add_post(self, idx, post):
        self.set_font('DejaVu', style='B', size=12)
        self.cell(0, 10, f"Inlägg {idx}", ln=True)
        self.set_font('DejaVu', size=12)
        self.multi_cell(0, 10, post)
        self.ln(10)

# Ladda ned PDF
if st.button("Ladda ned som PDF"):
    if not st.session_state["posts"]:
        st.warning("Ingen text att ladda ned.")
    else:
        # Generera PDF
        pdf = PDFWithUnicode()
        for idx, post in enumerate(st.session_state["posts"], 1):
            pdf.add_post(idx, post)

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
