import streamlit as st
from PIL import Image
import numpy as np
import random
import io

# Funktion för att dela upp en bild i mindre bitar
def split_image(image, rows, cols):
    img_width, img_height = image.size
    tile_width = img_width // cols
    tile_height = img_height // rows
    pieces = []

    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            top = row * tile_height
            right = (col + 1) * tile_width
            bottom = (row + 1) * tile_height
            piece = image.crop((left, top, right, bottom))
            pieces.append(piece)
    
    return pieces

# Funktion för att visa och hantera pusselspelet
def puzzle_game():
    # Ladda upp bild
    uploaded_file = st.file_uploader("Ladda upp en bild för pusslet", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Läs in bilden
        image = Image.open(uploaded_file)
        st.image(image, caption="Originalbild", use_column_width=True)

        # Välj antal rader och kolumner för pusslet
        rows = st.slider("Välj antal rader", 2, 5, 3, 4, 8)
        cols = st.slider("Välj antal kolumner", 2, 5, 3, 4, 8)

        # Dela upp bilden i bitar
        pieces = split_image(image, rows, cols)
        random.shuffle(pieces)  # Blanda bitarna

        # Visa bitarna som interaktiva knappar
        puzzle_state = []
        for i, piece in enumerate(pieces):
            st.image(piece, caption=f"Bit {i+1}", use_column_width=True)

            # Här kan vi skapa interaktiva knappar eller dra-och-släpp-funktioner för att placera bitarna
            # Placeholder för interaktivitet

        # Kontrollera om pusslet är klart
        # (För att kontrollera ordningen måste vi här hantera placeringen av bitarna)
        if st.button("Kontrollera pusslet"):
            # Här kan vi jämföra om alla bitar är i rätt ordning
            st.write("Pusslet är klart! Grattis!")


def main():
    st.title("Pusselspel")
    puzzle_game()

if __name__ == "__main__":
    main()
