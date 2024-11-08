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
            
            /* Flexbox för att placera ikonerna till vänster om texten */
            .icon-section {
                display: flex;
                align-items: flex-start;
                gap: 16px; /* Avstånd mellan ikon och text */
            }
            .icon-section .material-icons {
                font-size: 30px; /* Justera storlek på ikonen */
                color: #666; /* Färg för ikonen */
            }
            .icon-section h3 {
                margin: 0; /* Tar bort standardmarginal för att justera texten bättre */
            }
            .icon-section p {
                margin-top: 0; /* Tar bort extra marginal för justerad text */
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

# Första underrubriken med ikon och justerad layout
st.markdown("""
<div class="icon-section">
    <i class="material-icons">language</i>
    <div>
        <h4>Vad är en LLM eller språkmodell?</h4>
        <p>Kort info om LLM och språkmodeller.</p>
        <ul>
            <li>Punkt 1 under Underrubrik 2</li>
            <li>Punkt 2 under Underrubrik 2</li>
            <li>Punkt 3 under Underrubrik 2</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Andra underrubriken med ikon och justerad layout
st.markdown("""
<div class="icon-section">
    <i class="material-icons">token</i>
    <div>
        <h4>Vad är Prompt?</h4>
        <p>Kort beskrivning vad prompt är.</p>
        <ul>
            <li><a href="https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link" target="_blank">Här kan du ladda ned promptguiden</a></li>
            <li><a href="https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link" target="_blank">Här kan du ladda ned promptbiblioteket</a></li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Tredje underrubriken med ikon och justerad layout
st.markdown("""
<div class="icon-section">
    <i class="material-icons">hub</i>
    <div>
        <h4>Vad är BIAS</h4>
        <p>I maskininlärning och AI kan bias uppstå om algoritmer tränas på data som inte är helt rättvisande eller representativa. Om träningsdata har en snedvridning (till exempel att det finns fler exempel från en viss grupp människor än från andra) kan AI lära sig att fatta beslut som också är snedvridna. Detta innebär att AI kan gynna en viss grupp eller behandla andra grupper orättvist, vilket kan leda till orättvisa resultat eller slutsatser.</p>
        <ul>
            <li>AI kan bli snedvriden om träningsdata inte är rättvis eller representativ.</li>
            <li>Om datan är ojämnt fördelad mellan olika grupper, kan AI fatta orättvisa beslut.</li>
            <li>Detta kan leda till att vissa grupper gynnas, medan andra behandlas orättvist.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
