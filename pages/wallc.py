import streamlit as st
import os
import json
import random

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

# Funktion för att generera en slumpmässig ljus färg och dess mörkare variant
def generate_color():
    colors = {
        "green": (180, 255, 180, 60),
        "yellow": (255, 255, 180, 60),
        "red": (255, 180, 180, 60),
        "blue": (180, 180, 255, 60)
    }
    color_name = random.choice(list(colors.keys()))
    r, g, b, dark_diff = colors[color_name]
    light_color = f"rgb({r}, {g}, {b})"
    dark_color = f"rgb({max(r - dark_diff, 0)}, {max(g - dark_diff, 0)}, {max(b - dark_diff, 0)})"
    return light_color, dark_color

# Ladda tidigare inlägg
if "posts" not in st.session_state:
    st.session_state["posts"] = load_posts()

if "post_colors" not in st.session_state:
    st.session_state["post_colors"] = [generate_color() for _ in range(len(st.session_state["posts"]))]

if "post_states" not in st.session_state:
    st.session_state["post_states"] = ["default" for _ in range(len(st.session_state["posts"]))]

# Konfigurera sidan
st.set_page_config(page_title="Skapa och Dela Innehåll", layout="wide")

# Sidrubrik för att skapa inlägg
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
        st.session_state["post_colors"].append(generate_color())
        st.session_state["post_states"].append("default")
        save_posts(st.session_state["posts"])  # Spara inlägget till fil
        st.success("Ditt inlägg har publicerats!")
    else:
        st.warning("Inlägget kan inte vara tomt.")

# Funktion för att växla mellan färg och gråskala för ett inlägg
def toggle_post(idx):
    current_state = st.session_state["post_states"][idx]
    if current_state == "default":
        st.session_state["post_states"][idx] = "gray"
    elif current_state == "gray":
        st.session_state["post_states"][idx] = "default"

# Visa inlägg endast om lösenord är korrekt
password = st.text_input("Ange lösenord för att visa inlägg:", type="password")

if password == "hemligt":  # Ändra detta till ditt valda lösenord
    # Visa alla publicerade inlägg i tre kolumner
    if st.session_state["posts"]:
        columns = st.columns(3)  # Skapa tre kolumner
        for idx, post in enumerate(st.session_state["posts"]):
            col = columns[idx % 3]  # Välj kolumn baserat på index
            with col:
                light_color, dark_color = st.session_state["post_colors"][idx]
                current_state = st.session_state["post_states"][idx]

                if current_state == "gray":
                    style = "background-color:lightgray; border: 4px solid gray; padding:20px;"
                else:
                    style = f"background-color:{light_color}; border: 2px solid {dark_color}; padding:10px;"

                if st.button(f"Visa {idx+1}", key=f"btn_{idx}"):
                    toggle_post(idx)

                st.markdown(f"<div style='{style}'>{post}</div>", unsafe_allow_html=True)
    else:
        st.info("Inga inlägg har publicerats ännu.")
else:
    st.warning("Fel lösenord. Försök igen.")
