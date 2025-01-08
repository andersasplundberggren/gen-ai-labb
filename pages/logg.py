import streamlit as st
from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader

# Ladda in konfigurationsfil för autentisering
config = {
    'credentials': {
        'usernames': {}
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'random_signature_key',
        'name': 'auth_cookie'
    },
    'preauthorized': {
        'emails': []
    }
}

# Skapa autentiseringsobjekt
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Sidhuvud och autentisering
st.title("Skapa och Dela Innehåll")

# Inloggningsformulär
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.sidebar.write(f"Inloggad som {name}")
    authenticator.logout('Logga ut', 'sidebar')
    st.sidebar.success("Du är nu inloggad.")
    
    # Huvudinnehåll efter inloggning
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
    
    try:
        if authenticator.register_user('Skapa nytt konto', preauthorization=False):
            st.success('Konto skapat. Var vänlig logga in.')
    except Exception as e:
        st.error(e)
