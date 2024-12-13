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
    r, g, b = [random.randint(180, 255) for _ in range(3)]
    light_color = f"rgb({r}, {g}, {b})"
    dark_color = f"rgb({max(r - 60, 0)}, {max(g - 60, 0)}, {max(b - 60, 0)})"
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

# Funktion för att växla tillstånd för ett inlägg
def toggle_post(idx):
    current_state = st.session_state["post_states"][idx]
    if current_state == "default":
        st.session_state["post_states"][idx] = "enlarged"
    elif current_state == "enlarged":
        st.session_state["post_states"][idx] = "gray"
    elif current_state == "gray":
        st.session_state["post_states"][idx] = "enlarged"
    else:
        st.session_state["post_states"][idx] = "default"

# Visa alla publicerade inlägg i tre kolumner
if st.session_state["posts"]:
    columns = st.columns(3)  # Skapa tre kolumner
    for idx, post in enumerate(st.session_state["posts"]):
        col = columns[idx % 3]  # Välj kolumn baserat på index
        with col:
            light_color, dark_color = st.session_state["post_colors"][idx]
            current_state = st.session_state["post_states"][idx]

            if current_state == "enlarged":
                style = f"background-color:{light_color}; border: 4px solid {dark_color}; padding:20px; font-size:20px; cursor:pointer;"
            elif current_state == "gray":
                style = "background-color:lightgray; border: 4px solid gray; padding:20px; font-size:20px; cursor:pointer;"
            else:
                style = f"background-color:{light_color}; border: 2px solid {dark_color}; padding:10px; cursor:pointer;"

            button_html = f"""
            <div style="{style}" onclick="fetch('/?post_id={idx}', {{method: 'POST'}})">{post}</div>
            """
            st.markdown(button_html, unsafe_allow_html=True)

else:
    st.info("Inga inlägg har publicerats ännu.")
