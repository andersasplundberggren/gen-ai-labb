import streamlit as st
import hmac
import os
import config as c
from functions.styling import page_config, styling
from functions.menu import menu

### CSS AND STYLING ###

def styling():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
            
            /* Ikon och rubrik i samma rad */
            .icon-header {
                display: flex;
                align-items: center;
                gap: 8px; /* Justerar avståndet mellan ikon och text */
                font-family: 'Material Icons';
                font-size: 24px; /* Justera storlek på ikonen */
            }
            .icon-header i {
                color: #666; /* Valfri färg för ikoner */
            }
        </style>
    """, unsafe_allow_html=True)

# Konfiguration av sidan och styling
page_config()
styling()

# Kontrollera om språk är i session_state, annars sätt standardvärde
if 'language' not in st.session_state:
    st.session_state['language'] = "Svenska"  # Standard språk

st.session_state["pwd_on"] = st.secrets.pwd_on

### Lösenordsskydd ###

if st.session_state["pwd_on"] == "true":

    def check_password():
        if c.deployment == "streamlit":
            passwd = st.secrets["password"]
        else:
            passwd = os.environ.get("password")

        def password_entered():
            if hmac.compare_digest(st.session_state["password"], passwd):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Ta bort lösenordet efter inmatning.
            else:
                st.session_state["password_correct"] = False

        if st.session_state.get("password_correct", False):
            return True

        st.text_input("Lösenord", type="password", on_change=password_entered, key="password")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Ooops. Fel lösenord.")
        return False

    if not check_password():
        st.stop()

st.session_state["app_version"] = c.app_version
st.session_state["update_date"] = c.update_date

### Sidomeny ###
menu()

### Huvudsida ###

# Rubrik och välkomsttext
st.image("images/logome.png", width=200)
st.header("Välkommen till AILABBET")
st.write("Här kan du testa olika tjänster inom AI. Inget av det du gör här sparas, så om du får fram en bra text eller snygg bild får du se till att spara den.")

st.write("Här nedanför finns lite information som kan vara bra att ha koll på innan du kör igång.")

# Första underrubriken med ikon
st.markdown('<div class="icon-header"><i class="material-icons">info</i><h3>Vad är en LLM eller språkmodell?</h3></div>', unsafe_allow_html=True)
st.write("Kort info om LLM och språkmodeller.")
st.markdown("""
- Punkt 1 under Underrubrik 2
- Punkt 2 under Underrubrik 2
- Punkt 3 under Underrubrik 2
""")

# Andra underrubriken med ikon
st.markdown('<div class="icon-header"><i class="material-icons">question_answer</i><h3>Vad är Prompt?</h3></div>', unsafe_allow_html=True)
st.write("Kort beskrivning vad prompt är.")
st.markdown("""
   - <a href="https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link" target="_blank">Här kan du ladda ned promptguiden</a>  
   - <a href="https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link" target="_blank">Här kan du ladda ned promptbiblioteket</a>  
""", unsafe_allow_html=True)

# Tredje underrubriken med ikon
st.markdown('<div class="icon-header"><i class="material-icons">warning</i><h3>Vad är BIAS</h3></div>', unsafe_allow_html=True)
st.write("Kort info om BIAS")
st.markdown("""
- Punkt 1 under Underrubrik 3
- Punkt 2 under Underrubrik 3
- Punkt 3 under Underrubrik 3
""")
