import streamlit as st
import random

# Funktion för att skapa och hantera Memory-spelet
def memory_game():
    # Speldata - en lista med kort (kan vara text eller bilder)
    cards = ["A", "B", "C", "D", "E", "F", "A", "B", "C", "D", "E", "F"]
    random.shuffle(cards)  # Blanda korten för varje omgång

    # Hantera spelstillstånd
    if "flipped_cards" not in st.session_state:
        st.session_state.flipped_cards = []  # Håller reda på de omvända korten
        st.session_state.matched_cards = []  # Håller reda på de matchade korten
        st.session_state.attempts = 0  # Försök gjorda

    # Visa korten i en 4x3 matris
    rows = 4
    cols = 3
    card_index = 0
    buttons = []

    # Skapa knappar för varje kort
    for row in range(rows):
        cols_list = []
        for col in range(cols):
            if card_index < len(cards):
                # Kontrollera om kortet är omvänt eller redan matchat
                if card_index in st.session_state.matched_cards:
                    display = cards[card_index]  # Kortet har matchats
                elif card_index in st.session_state.flipped_cards:
                    display = cards[card_index]  # Kortet är vänt
                else:
                    display = "?"  # Kortet är dolt

                # Skapa en knapp för kortet
                button = st.button(display, key=f"card_{card_index}")
                if button:
                    # När knappen trycks, vänd kortet
                    st.session_state.flipped_cards.append(card_index)

                cols_list.append(button)
                card_index += 1
        st.write(cols_list)  # Skriver ut kolumner med kort

    # Kontrollera om två kort är vända
    if len(st.session_state.flipped_cards) == 2:
        card1, card2 = st.session_state.flipped_cards
        if cards[card1] == cards[card2]:  # Om korten matchar
            st.session_state.matched_cards.append(card1)
            st.session_state.matched_cards.append(card2)
        st.session_state.flipped_cards = []  # Töm listan på omvända kort
        st.session_state.attempts += 1

    # Visa feedback
    if len(st.session_state.matched_cards) == len(cards):
        st.success(f"Grattis! Du har matchat alla kort på {st.session_state.attempts} försök.")
    else:
        st.write(f"Försök: {st.session_state.attempts}")

# Starta spelet
def main():
    st.title("Memory Game")
    memory_game()

if __name__ == "__main__":
    main()
