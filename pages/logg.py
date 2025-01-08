import streamlit as st
import yaml
from yaml.loader import SafeLoader
import bcrypt

# Ladda eller skapa användarkonfiguration
CONFIG_FILE = 'user_config.yaml'

# Ladda användardata
try:
    with open(CONFIG_FILE, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    config = {'users': {}}

# Spara användardata
def save_config():
    with open(CONFIG_FILE, 'w') as file:
        yaml.dump(config, file)

# Hasha lösenord
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Verifiera lösenord
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Inloggningsstatus
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# Inloggningsformulär
st.title("Skapa och Dela Innehåll")

if st.session_state['authentication_status']:
    st.sidebar.write(f"Inloggad som {st.session_state['username']}")
    if st.sidebar.button('Logga ut'):
        st.session_state['authentication_status'] = None
        st.session_state['username'] = ''
        st.experimental_rerun()
    
    st.markdown("### Dokumentera")

    user_text = st.text_area(
        label="Lägg till text",
        placeholder="Skriv något intressant...",
        height=200
    )

    uploaded_images = st.file_uploader(
        label="Ladda upp bilder",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if st.button("Visa innehåll"):
        st.markdown("### Innehåll")
        if user_text:
            st.markdown(user_text)
        if uploaded_images:
            for image in uploaded_images:
                st.image(image, caption=image.name)
else:
    st.sidebar.write("Inte inloggad")
    login_username = st.text_input("Användarnamn")
    login_password = st.text_input("Lösenord", type="password")
    
    if st.button("Logga in"):
        if login_username in config['users']:
            if verify_password(login_password, config['users'][login_username]['password']):
                st.session_state['authentication_status'] = True
                st.session_state['username'] = login_username
                st.experimental_rerun()
            else:
                st.error("Fel lösenord.")
        else:
            st.error("Användarnamn hittades inte.")
    
    st.markdown("---")
    st.markdown("### Skapa nytt konto")
    new_username = st.text_input("Nytt användarnamn")
    new_password = st.text_input("Nytt lösenord", type="password")
    confirm_password = st.text_input("Bekräfta lösenord", type="password")

    if st.button("Registrera"):
        if new_username in config['users']:
            st.error("Användarnamnet är redan taget.")
        elif new_password != confirm_password:
            st.error("Lösenorden matchar inte.")
        else:
            hashed_password = hash_password(new_password)
            config['users'][new_username] = {'password': hashed_password}
            save_config()
            st.success("Konto skapat. Logga in ovan.")
