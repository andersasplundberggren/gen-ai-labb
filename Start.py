import streamlit as st
import hmac
import os
import config as c
from functions.styling import page_config, styling
from functions.menu import menu

### CSS AND STYLING ###

st.logo("images/logome.png", icon_image="images/logo_small.png")

# Sidkonfiguration och styling
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
                del st.session_state["password"]
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

# CSS för att ge expander-boxarna en ljusblå bakgrund
st.markdown("""
    <style>
    .st-expander > div:first-child {
        background-color: #e0f7fa; /* Ljusblå bakgrundsfärg */
        border-radius: 12px; /* Rundade hörn */
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Utfällbara sektioner
with st.expander("Generativ AI, say what!?"):
    st.write("""
        Generativ AI är en typ av artificiell intelligens som kan skapa nytt innehåll – som texter, bilder, musik eller kod – istället för att bara analysera eller bearbeta redan existerande data. 
        Den fungerar genom att lära sig av stora mängder data, som exempelvis miljontals bilder eller texter, för att sedan kunna producera något som liknar det den lärt sig. 
        Många gånger kan generativ AI nästan upplevas som mänsklig intelligens.
    """)
    st.markdown("""
        - *Generativ AI kan skapa text, bilder och musik istället för att bara analysera saker.*
        - **AI tränas med massor av exempel som texter och bilder för att förstå mönster.**
        - **När man ställer en fråga eller ger en instruktion, skapar AI nytt innehåll utifrån vad den har lärt sig.**
    """)

with st.expander("Vad är en LLM eller språkmodell?"):
    st.write("""
        En språkmodell eller LLM (Large Language Model) är en typ av AI som tränas på enorma mängder text för att förstå och generera mänskligt språk. 
        Dessa modeller kan skapa text, svara på frågor och hjälpa med olika språkliga uppgifter genom att identifiera mönster i datan de har tränats på. 
        LLM används ofta i chatbots, översättningstjänster och andra system som kräver förståelse och generering av text. 
        De är kraftfulla, men kan också spegla och förstärka snedvridningar i den data de tränas på.
    """)
    st.markdown("""
        - **En LLM är en AI som tränas på stora mängder text för att förstå och skapa mänskligt språk.**
        - **En LLM används för att generera text, svara på frågor och utföra språkliga uppgifter.**
        - **Viktigt att tänka på. En LLM kan spegla snedvridningar i träningsdata, vilket kan leda till bias eller orättvisa resultat.**
    """)

with st.expander("Vad är Prompt?"):
    st.write("""
        En prompt är en instruktion eller fråga som du ger till en AI för att få ett svar eller en åtgärd. 
        Det är det du skriver in för att "be" AI göra något, som att generera text, svara på en fråga eller skapa en bild. 
        Till exempel, om du skriver "Skriv en berättelse om en drake", så är det en prompt som AI svarar på genom att skapa en berättelse.
        Här nedför kan du ladda ned en promptguide och ett promptbibliotek framtaget av RISE som kan ge dig lite vägledning kring hur du kan prompta på ett effektivt sätt.
    """)
    st.markdown("""
        - [Här kan du ladda ned promptguiden](https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link)
        - [Här kan du ladda ned promptbiblioteket](https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link)
    """)

with st.expander("Vad är BIAS?"):
    st.write("""
        I maskininlärning och AI kan bias uppstå om algoritmer tränas på data som inte är helt rättvisande eller representativa. 
        Om träningsdata har en snedvridning (till exempel att det finns fler exempel från en viss grupp människor än från andra) kan AI lära sig att fatta beslut som också är snedvridna. 
        Detta innebär att AI kan gynna en viss grupp eller behandla andra grupper orättvist, vilket kan leda till orättvisa resultat eller slutsatser.
    """)
    st.markdown("""
        - **AI kan bli snedvriden om träningsdata inte är rättvis eller representativ.**
        - **Om datan är ojämnt fördelad mellan olika grupper, kan AI fatta orättvisa beslut.**
        - **Detta kan leda till att vissa grupper gynnas, medan andra behandlas orättvist.**
    """)

with st.expander("Kostar det något att använda AI?"):
    st.write("""
        Att använda AI kostar en slant men hur mycket kostar det egentligen? Det enkla, men långt ifrån bästa, svaret är. Det beror på. 
        Du kan skaffa en pluslicens på ChatGPT där du kan chatta och generera bilder obegränsat för 250 kronor per månad. 
        Tjänsten på den här sidan är istället skapad där betalning sker löpande baserat på nyttjande av **tokens**.
        
        I AI-sammanhang är en token en liten del av text, som kan vara ett ord, en del av ett ord eller till och med ett enstaka tecken. 
        När en AI-modell, som exempelvis en språkmodell, bearbetar text, bryter den ner texten till dessa små enheter (tokens) för att bättre kunna förstå och generera språk.
        
        Istället för att behandla hela meningen på en gång analyserar modellen varje token separat och bedömer vilken token som ska komma härnäst. 
        Det gör att modellen kan hantera både korta och längre textsträngar effektivt. Beroende på vilken språkmodell som används så är priset olika. 
        Om vi tar ett exempel där vi använder GPT-4o som är den senaste språkmodellen så betalar vi 2.5 dollar för en miljon tokens. 
        Som jämförelse innehåller kommunallagen med sina drygt 100 000 tecken typ 36 000 tokens. Om vi genererar bilder eller behandlar ljud blir kostnaden högre.
    """)
    st.markdown("""
        - **Att använda AI kostar en slant men inga jättesummor.**
        - **Text är billigare än ljud och bild.**
    """)
