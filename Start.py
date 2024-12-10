import streamlit as st
import hmac
import os
import config as c
from functions.styling import page_config, styling
from functions.menu import menu

# Sidkonfiguration och styling

st.logo("images/logome.png", icon_image = "images/logo_small.png")

page_config()
styling()

# Kontrollera om språk är i session_state, annars sätt standardvärde
if 'language' not in st.session_state:
    st.session_state['language'] = "Svenska"  # Standard språk

st.session_state["pwd_on"] = st.secrets.pwd_on

# Lösenordsskydd
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

# Sidomeny
menu()

# Huvudsida
st.image("images/logome.png", width=200)
st.header("Välkommen till AILABBET")

st.write("Här nedanför finns lite information som kan vara bra att ha koll på innan du kör igång.")

# Expanderbara sektioner med ljusblå bakgrund
sections = [
    ("Generativ AI, say what!?", """
        Generativ AI är en typ av artificiell intelligens som kan skapa nytt innehåll – som texter, bilder, musik eller kod – istället för att bara analysera eller bearbeta redan existerande data.
        Den fungerar genom att lära sig av stora mängder data, som exempelvis miljontals bilder eller texter, för att sedan kunna producera något som liknar det den lärt sig.
        Många gånger kan generativ AI nästan upplevas som mänsklig intelligens.

        - Generativ AI kan skapa text, bilder och musik istället för att bara analysera saker.
        - AI tränas med massor av exempel som texter och bilder för att förstå mönster.
        - När man ställer en fråga eller ger en instruktion, skapar AI nytt innehåll utifrån vad den har lärt sig.
    
    """),

      ("Vad är en LLM eller språkmodell?", """
        En språkmodell eller LLM (Large Language Model) är en typ av AI som tränas på enorma mängder text för att förstå och generera mänskligt språk.
        Dessa modeller kan skapa text, svara på frågor och hjälpa med olika språkliga uppgifter genom att identifiera mönster i datan de har tränats på.
        LLM används ofta i chatbots, översättningstjänster och andra system som kräver förståelse och generering av text.
        De är kraftfulla, men kan också spegla och förstärka snedvridningar i den data de tränas på.

        - En LLM är en AI som tränas på stora mängder text för att förstå och skapa mänskligt språk.
        - En LLM används för att generera text, svara på frågor och utföra språkliga uppgifter.
        - Viktigt att tänka på. En LLM kan spegla snedvridningar i träningsdata, vilket kan leda till bias eller orättvisa resultat.
    """),
    
    # ("OpenAI & LLaMa. Vad är vad?", """
        OpenAI GPT och LLaMA är båda avancerade språkmodeller, skapade av olika företag, och är designade för att förstå och generera text på ett naturligt sätt. Båda modellerna är exempel på hur AI och maskininlärning används för att skapa kraftfulla verktyg som kan hjälpa inom många områden – från kundtjänst och automatisering till kreativt skrivande och forskning.

        - OpenAI - GPT-modeller (Generative Pre-trained Transformer) är en serie av stora språkmodeller. Dessa modeller är tränade på enorma mängder textdata och kan generera text, svara på frågor, översätta språk, och utföra många andra textbaserade uppgifter. OpenAI har släppt flera versioner, där de mest kända är GPT-3 och GPT-4. Modellen fungerar så att den förutspår nästa ord i en sekvens baserat på tidigare ord, vilket gör att den kan generera sammanhängande och realistiska svar på en rad olika frågor och instruktioner.
        - LLaMA - Språkmodeller utvecklade av Meta (tidigare Facebook). LLaMA-modellerna är designade för att vara högpresterande men mer resurssnåla jämfört med andra stora språkmodeller, vilket gör dem enklare att köra på mindre enheter och för specifika uppgifter. Meta har släppt flera versioner, inklusive LLaMA 1 och 2. LLaMA har designats för att vara forskningsvänlig, och den släpps oftast som öppen källkod, vilket ger forskare och utvecklare möjlighet att studera och vidareutveckla modellen.
    """),
  
    ("Vad är Prompt?", """
        En prompt är en instruktion eller fråga som du ger till en AI för att få ett svar eller en åtgärd.
        Det är det du skriver in för att "be" AI göra något, som att generera text, svara på en fråga eller skapa en bild.
        Till exempel, om du skriver "Skriv en berättelse om en drake", så är det en prompt som AI svarar på genom att skapa en berättelse.
        Här nedför kan du ladda ned en promptguide och ett promptbibliotek framtaget av RISE som kan ge dig lite vägledning kring hur du kan prompta på ett effektivt sätt.

        - [Ladda ned promptguiden](https://drive.google.com/file/d/1f-vytD_xPwdrKudjD4mlq9rx08GcGoN3/view?usp=drive_link)
        - [Ladda ned promptbiblioteket](https://drive.google.com/file/d/1VTRN4j6GxVWV9hHIeJM-kabzieTOHosq/view?usp=drive_link)
    """),
    ("Vad är BIAS?", """
        I maskininlärning och AI kan bias uppstå om algoritmer tränas på data som inte är helt rättvisande eller representativa.
        Om träningsdata har en snedvridning (till exempel att det finns fler exempel från en viss grupp människor än från andra) kan AI lära sig att fatta beslut som också är snedvridna.
        Detta innebär att AI kan gynna en viss grupp eller behandla andra grupper orättvist, vilket kan leda till orättvisa resultat eller slutsatser.

        - AI kan bli snedvriden om träningsdata inte är rättvis eller representativ.
        - Om datan är ojämnt fördelad mellan olika grupper, kan AI fatta orättvisa beslut.
        - Detta kan leda till att vissa grupper gynnas, medan andra behandlas orättvist.
    """),
    ("Kostar det något att använda AI?", """
        Att använda AI kostar en slant men hur mycket kostar det egentligen? Det enkla, men långt ifrån bästa, svaret är. Det beror på.
        Du kan skaffa en pluslicens på ChatGPT där du kan chatta och generera bilder obegränsat för 250 kronor per månad.
        Tjänsten på den här sidan är istället skapad där betalning sker löpande baserat på nyttjande av **tokens**.
        
        I AI-sammanhang är en token en liten del av text, som kan vara ett ord, en del av ett ord eller till och med ett enstaka tecken.
        När en AI-modell, som exempelvis en språkmodell, bearbetar text, bryter den ner texten till dessa små enheter (tokens) för att bättre kunna förstå och generera språk.
        Att dela texten i tokens gör det lättare för AI att bearbeta språket.
        Istället för att behandla hela meningen på en gång analyserar modellen varje token separat och bedömer vilken token som ska komma härnäst.
        Det gör att modellen kan hantera både korta och längre textsträngar effektivt.
        
        Beroende på vilken språkmodell som används så är priset olika.
        Om vi tar ett exempel där vi använder GPT-4o som är den senaste språkmodellen så betalar vi 2.5 dollar för en miljon tokens.
        Som jämförelse innehåller kommunallagen med sina drygt 100 000 tecken typ 36 000 tokens.
        Om vi genererar bilder eller behandlar ljud blir kostnaden högre.

        - Att använda AI kostar en slant men inga jättesummor.
        - Arbete med text är billigare än ljud och bild.
    """)
]

# Generera expanderbara sektioner
for title, content in sections:
    with st.expander(title):
        st.markdown(f"""
            <div style="background-color: #e0f7fa; border-radius: 12px; padding: 10px;">
                {content}
            </div>
        """, unsafe_allow_html=True)

st.write("I menyn till vänster kan du testa olika tjänster inom AI. Inget av det du gör här sparas, så om du får fram en bra text eller snygg bild får du se till att spara den. Tänk på att detta är en prototyp där information du matar in bearbetas med en språkmodell. Prototypen är inte GDPR-säkrad och använder AI-modeller som körs på servrar i USA.")

st.write(" ")
