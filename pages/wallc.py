import streamlit as st
import random

# Spel 1: Gissa numret
def guess_number_game():
    st.title("Gissa numret!")
    number = random.randint(1, 100)
    guess = None
    attempts = 0

    while guess != number:
        guess = st.number_input("Gissa ett tal mellan 1 och 100", min_value=1, max_value=100, key=f"guess_{attempts}")
        if guess < number:
            st.write("För lågt!")
        elif guess > number:
            st.write("För högt!")
        attempts += 1

    st.write(f"Grattis! Du gissade rätt på {attempts} försök.")

# Spel 2: Hänga gubbe
def hangman_game():
    st.title("Hänga gubbe!")
    word = random.choice(["python", "streamlit", "programming", "hangman"])
    guessed_letters = set()
    attempts = 6

    while attempts > 0:
        word_display = "".join([letter if letter in guessed_letters else "_" for letter in word])
        guess = st.text_input(f"Ord: {word_display} - Gissa en bokstav", max_chars=1)
        
        if guess:
            if guess in word:
                guessed_letters.add(guess)
                st.write(f"Bra jobbat! {guess} är i ordet.")
            else:
                attempts -= 1
                st.write(f"Fel! Du har {attempts} försök kvar.")
        
        if all(letter in guessed_letters for letter in word):
            st.write(f"Grattis! Du gissade ordet: {word}")
            break
    else:
        st.write(f"Du förlorade! Ordet var: {word}")

# Spel 3: Tic-Tac-Toe
def tic_tac_toe_game():
    st.title("Tic-Tac-Toe")
    # Här kan du lägga till en enkel logik för Tic-Tac-Toe-spelet
    # T.ex. skapa ett rutnät och hantera användarens drag.

# Spelmeny
def main():
    st.sidebar.title("Välj ett spel")
    game_choice = st.sidebar.selectbox("Välj ett spel", ["Gissa numret", "Hänga gubbe", "Tic-Tac-Toe"])

    if game_choice == "Gissa numret":
        guess_number_game()
    elif game_choice == "Hänga gubbe":
        hangman_game()
    elif game_choice == "Tic-Tac-Toe":
        tic_tac_toe_game()

if __name__ == "__main__":
    main()
