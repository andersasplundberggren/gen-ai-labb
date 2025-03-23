# External imports
import streamlit as st
from llama_index.core.llms import ChatMessage
from openai import OpenAI
from groq import Groq
import requests
from bs4 import BeautifulSoup
import re

# Python imports
import hmac
import os
from os import environ

# Local imports 
from functions.styling import page_config, styling
from functions.menu import menu
import config as c

### CSS AND STYLING

st.logo("images/logome.png", icon_image = "images/logo_small.png")

page_config()
styling()

# Skapa flikar för olika funktioner
tab1, tab2 = st.tabs(["Chat", "Webbsida översättning"])

with tab1:
    # Utfällbar textruta med bilder och punktlista
    with st.expander("### Övning"):  # Gör rubriken lika stor som underrubriken
        st.markdown("""
            ### Sammanfatta text och skapa quiz:
            - Gå till Wikipedia och hitta en artikel.
            - Markera och kopiera texten från artikeln.
            - Klistra in texten och skriv en prompt för att be chatbotten summera artikeln.
            - Skriv in prompt där du ber om en quiz med 10 frågor baserat på innehållet i texten.
        """)
        
        st.write("Tips. Skriv din prompt gör sedan radbryt med hjälp av shift + enter och skriv in tre --- och efter det ytterligare ett radbryt med shift + enter. Klistra sedan in texten som du kopierat. Du kan även testa att kopiera länken till sidan på Wikipedia och därefter skriva in din prompt.")
        
         # Lägg till en bild
        #st.image("images/me.png", caption="Lycka till!")

    # Check if language is already in session_state, else initialize it with a default value
    if 'language' not in st.session_state:
        st.session_state['language'] = "Svenska"  # Default language

    st.session_state["pwd_on"] = st.secrets.pwd_on

    ### PASSWORD

    if st.session_state["pwd_on"] == "true":

        def check_password():

            if c.deployment == "streamlit":
                passwd = st.secrets["password"]
            else:
                passwd = environ.get("password")

            def password_entered():

                if hmac.compare_digest(st.session_state["password"], passwd):
                    st.session_state["password_correct"] = True
                    del st.session_state["password"]  # Don't store the password.
                else:
                    st.session_state["password_correct"] = False

            if st.session_state.get("password_correct", False):
                return True

            st.text_input("Lösenord", type="password", on_change=password_entered, key="password")
            if "password_correct" in st.session_state:
                st.error("😕 Ooops. Fel lösenord.")
            return False


        if not check_password():
            st.stop()
            
    ### ### ### ###


    # Translation

    if st.session_state['language'] == "Svenska":
        chat_prompt = "Du är en hjälpsam AI-assistent. Svara på användarens frågor."
        chat_clear_chat = "Rensa chat"
        chat_hello = "Hej! Hur kan jag hjälpa dig?"
        chat_settings = "Inställningar"
        chat_choose_llm = "Välj språkmodell"
        chat_choose_temp = "Temperatur"
        chat_system_prompt = "Systemprompt"
        chat_save = "Spara"
        chat_imput_q = "Vad vill du prata om?"

    elif st.session_state['language'] == "English":
        chat_prompt = "You are a helpful AI assistant. Answer the user's questions."
        chat_clear_chat = "Clear chat"
        chat_hello = "Hi! How can I help you?"
        chat_settings = "Settings"
        chat_choose_llm = "Choose language model"
        chat_choose_temp = "Temperature"
        chat_system_prompt = "System prompt"
        chat_save = "Save"
        chat_imput_q = "What do you want to talk about?"


    prompt = f"{chat_prompt}"


    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = prompt


    # Check and set default values if not set in session_state
    if "llm_temperature" not in st.session_state:
        st.session_state["llm_temperature"] = 0.7
    if "llm_chat_model" not in st.session_state:
        st.session_state["llm_chat_model"] = "OpenAI GPT-4o mini"


    ### SIDEBAR

    menu()

    st.sidebar.warning("""Det här är en prototyp där information du matar in 
                           bearbetas med en språkmodell. 
                           Prototypen är __inte GDPR-säkrad__, då den använder AI-modeller 
                           som körs på servrar i USA.""")


    ### MAIN PAGE

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"{chat_clear_chat}", type="secondary"):
            if "messages" in st.session_state.keys(): # Initialize the chat message history
                st.session_state.messages = [
                    {"role": "assistant", "content": f"""
                        {chat_hello}
                     """}
            ]

    with col2:
        with st.expander(f"{chat_settings}"):
            llm_model = st.selectbox(
                f"{chat_choose_llm}", 
                ["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"],
                index=["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"].index(st.session_state["llm_chat_model"]),
            )

            llm_temp = st.slider(
                f"{chat_choose_temp}",
                min_value = 0.0,
                max_value = 1.0,
                step = 0.1,
                value = st.session_state["llm_temperature"],
            )

            # Update the session_state directly
            st.session_state["llm_chat_model"] = llm_model
            st.session_state["llm_temperature"] = llm_temp
            
            model_map = {
                "OpenAI GPT-4o": "gpt-4o",
                "OpenAI GPT-4o mini": "gpt-4o-mini",
                "OpenAI o1-preview": "o1-preview", 
                "OpenAI o1-mini": "o1-mini"
            }

            st.markdown("###### ")

            with st.form("my_form"):
                prompt_input = st.text_area(f"{chat_system_prompt}", prompt, height=200)
                st.session_state.system_prompt = prompt_input   
                st.form_submit_button(f"{chat_save}") 


    if "OpenAI" in st.session_state["llm_chat_model"]:
        st.sidebar.success("Språkmodell: " + llm_model)
    else:
        st.sidebar.success("Språkmodell: " + llm_model)


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": f"{chat_hello}"}]


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Check if the content is an image URL
            if message["content"].startswith("http"):
                st.image(message["content"])
            else:
                st.markdown(message["content"])


    # Define your system prompt here
    system_prompt = st.session_state.system_prompt

    if prompt := st.chat_input(f"{chat_imput_q}"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Preprocess messages to include the system prompt
            processed_messages = []
            for m in st.session_state.messages:
                # Prepend system prompt to the user's message
                if m["role"] == "user":
                    content_with_prompt = system_prompt + " " + m["content"]
                    processed_messages.append({"role": m["role"], "content": content_with_prompt})
                else:
                    processed_messages.append(m)

            if "OpenAI" in st.session_state["llm_chat_model"]:

                if c.deployment == "streamlit":
                    client = OpenAI(api_key = st.secrets.openai_key)
                else:
                    client = OpenAI(api_key = environ.get("openai_key"))
        
                for response in client.chat.completions.create(
                    model = model_map[st.session_state["llm_chat_model"]],
                    temperature = st.session_state["llm_temperature"],
                    messages = processed_messages,
                    stream = True,
                ):
                    if response.choices[0].delta.content:
                        full_response += str(response.choices[0].delta.content)
                    message_placeholder.markdown(full_response + "▌")  
                 
            else:

                if c.deployment == "streamlit":
                    client = Groq(api_key = st.secrets.groq_key)
                else:
                    client = Groq(api_key = environ.get("groq_key"))

                # Remove 'avatar' key for Groq messages
                processed_messages_no_avatar = [{"role": m["role"], "content": m["content"]} for m in processed_messages]
                stream = client.chat.completions.create(
                    messages=processed_messages_no_avatar,
                    model=model_map[st.session_state["llm_chat_model"]],
                    temperature=st.session_state["llm_temperature"],
                    max_tokens=1024,
                    top_p=1,
                    stop=None,
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += str(chunk.choices[0].delta.content)
                    message_placeholder.markdown(full_response + "▌")
                    
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Fliken för översättning och sammanfattning av webbsidor
with tab2:
    st.header("Översätt och sammanfatta webbsida")
    
    # Skapa eller hämta session state för översättning
    if "web_url" not in st.session_state:
        st.session_state.web_url = ""
    if "web_content" not in st.session_state:
        st.session_state.web_content = {"original": "", "translated": "", "summary": ""}
    if "web_loading" not in st.session_state:
        st.session_state.web_loading = False
    
    # Formulär för URL-inmatning
    with st.form("web_form"):
        url = st.text_input("Webbadress (URL)", placeholder="https://exempel.com", value=st.session_state.web_url)
        submit_button = st.form_submit_button("Översätt och sammanfatta")
    
    # När formuläret skickas
    if submit_button:
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            st.error("Vänligen ange en giltig URL som börjar med http:// eller https://")
        else:
            st.session_state.web_url = url
            st.session_state.web_loading = True
            
            try:
                # Hämta webbinnehåll
                response = requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                })
                response.raise_for_status()  # Kasta fel om statusen inte är 200
                
                # Analysera HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Ta bort skript och stilelement
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Extrahera text
                text = soup.get_text()
                
                # Rensa extra mellanslag och tomma rader
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                # Begränsa längden (OpenAI har begränsningar för indata)
                max_chars = 10000
                if len(text) > max_chars:
                    text = text[:max_chars] + "... (innehållet trunkerat pga. längdbegränsningar)"
                
                # Använd AI för översättning och sammanfattning
                if c.deployment == "streamlit":
                    client = OpenAI(api_key = st.secrets.openai_key)
                else:
                    client = OpenAI(api_key = environ.get("openai_key"))
                
                # För översättning
                translation_prompt = [
                    {"role": "system", "content": "Du är en översättare som översätter text från alla språk till svenska. Behåll struktur och formatering så nära originalet som möjligt."},
                    {"role": "user", "content": f"Översätt följande text till svenska: \n\n{text}"}
                ]
                
                translation_response = client.chat.completions.create(
                    model = model_map[st.session_state["llm_chat_model"]],
                    temperature = 0.3,
                    messages = translation_prompt
                )
                translated_text = translation_response.choices[0].message.content
                
                # För sammanfattning
                summary_prompt = [
                    {"role": "system", "content": "Du är en assistent som skapar koncisa och informativa sammanfattningar av text."},
                    {"role": "user", "content": f"Skapa en kort sammanfattning av följande text på svenska. Fokusera på de viktigaste punkterna och ge en bra överblick av innehållet: \n\n{translated_text}"}
                ]
                
                summary_response = client.chat.completions.create(
                    model = model_map[st.session_state["llm_chat_model"]],
                    temperature = 0.3,
                    messages = summary_prompt
                )
                summary_text = summary_response.choices[0].message.content
                
                # Spara resultaten
                st.session_state.web_content = {
                    "original": text,
                    "translated": translated_text,
                    "summary": summary_text
                }
                
            except Exception as e:
                st.error(f"Ett fel uppstod: {str(e)}")
            
            finally:
                st.session_state.web_loading = False
    
    # Visa laddningsindikator
    if st.session_state.web_loading:
        st.info("Hämtar innehåll, översätter och sammanfattar...")
        progress_bar = st.progress(0)
        for i in range(100):
            # Simulera framsteg
            time.sleep(0.01)
            progress_bar.progress(i + 1)
    
    # Visa resultat
    if st.session_state.web_content["original"] and not st.session_state.web_loading:
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("Originaltext", expanded=False):
                st.markdown(st.session_state.web_content["original"])
        
        with col2:
            with st.expander("Svensk översättning", expanded=True):
                st.markdown(st.session_state.web_content["translated"])
        
        st.subheader("Sammanfattning")
        st.markdown(st.session_state.web_content["summary"])
        
        # Nedladdningsknappar
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.download_button("Ladda ner originaltext", st.session_state.web_content["original"], "originaltext.txt"):
                st.success("Originaltext nedladdad!")
        with col2:
            if st.download_button("Ladda ner översättning", st.session_state.web_content["translated"], "översättning.txt"):
                st.success("Översättning nedladdad!")
        with col3:
            if st.download_button("Ladda ner sammanfattning", st.session_state.web_content["summary"], "sammanfattning.txt"):
                st.success("Sammanfattning nedladdad!")
