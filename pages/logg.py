import streamlit as st
import sqlite3
import hashlib

# Skapa databasanslutning och tabeller
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    is_admin BOOLEAN
)''')
conn.commit()

# Hashfunktion

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registrering av användare

def register_user(username, password, is_admin=False):
    c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', 
              (username, hash_password(password), is_admin))
    conn.commit()

# Kontrollera användare

def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
              (username, hash_password(password)))
    return c.fetchone()

# Kontrollera om admin

def is_admin(username):
    c.execute('SELECT is_admin FROM users WHERE username = ?', (username,))
    return c.fetchone()[0]

# Huvudapplikation

def main():
    st.title("Användarhantering med Streamlit")

    menu = ["Logga in", "Registrera", "Admin"]
    choice = st.sidebar.selectbox("Meny", menu)

    if choice == "Logga in":
        st.subheader("Logga in")
        username = st.text_input("Användarnamn")
        password = st.text_input("Lösenord", type="password")

        if st.button("Logga in"):
            result = authenticate_user(username, password)
            if result:
                st.success(f"Välkommen {username}!")
                if is_admin(username):
                    st.info("Du är inloggad som administratör.")
            else:
                st.warning("Fel användarnamn eller lösenord")

    elif choice == "Registrera":
        st.subheader("Registrera ny användare")
        new_user = st.text_input("Användarnamn")
        new_password = st.text_input("Lösenord", type="password")
        admin_checkbox = st.checkbox("Är admin")

        if st.button("Registrera"):
            if new_user and new_password:
                try:
                    register_user(new_user, new_password, admin_checkbox)
                    st.success("Registrering lyckades")
                except Exception as e:
                    st.warning("Användarnamnet är redan upptaget")
            else:
                st.warning("Fyll i alla fält")

    elif choice == "Admin":
        st.subheader("Adminpanel")
        admin_user = st.text_input("Admin-användarnamn")
        admin_pass = st.text_input("Admin-lösenord", type="password")

        if st.button("Logga in som admin"):
            result = authenticate_user(admin_user, admin_pass)
            if result and is_admin(admin_user):
                st.success("Inloggning som admin lyckades")
                st.subheader("Hantera användare")
                c.execute('SELECT username, is_admin FROM users')
                users = c.fetchall()
                for user in users:
                    st.write(f"{user[0]} - {'Admin' if user[1] else 'Användare'}")
            else:
                st.warning("Ej behörig eller fel lösenord")

if __name__ == '__main__':
    main()
