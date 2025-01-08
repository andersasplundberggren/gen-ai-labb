import streamlit as st
import sqlite3
import hashlib

# Skapa databasanslutning och tabeller
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Skapa tabell om den inte finns
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        is_admin BOOLEAN
    )''')
    conn.commit()

# Rensa användartabellen (endast för ny installation)
def reset_users_table():
    c.execute('DROP TABLE IF EXISTS users')
    conn.commit()
    create_table()

# Skapa admin om inte redan finns
def create_admin():
    admin_username = "admin"
    admin_password = "admin123"
    c.execute('SELECT * FROM users WHERE username = ?', (admin_username,))
    if not c.fetchone():
        c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', 
                  (admin_username, hash_password(admin_password), True))
        conn.commit()

# Hashfunktion
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registrera användare
def register_user(username, password):
    c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', 
              (username, hash_password(password), False))
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

# Ta bort användare
def delete_user(username):
    c.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()

# Hämta alla användare
def get_users():
    c.execute('SELECT username, is_admin FROM users')
    return c.fetchall()

# Huvudapplikation
def main():
    st.title("Användarhantering med Streamlit")

    # Första gången applikationen körs ska användartabellen rensas
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        reset_users_table()  # Återställ databasen om det är första gången

    # Skapa admin om inte finns
    create_admin()

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
                    st.subheader("Hantera ditt konto")
                    if st.button("Ta bort mitt konto"):
                        if st.confirm("Är du säker på att du vill ta bort ditt konto? Detta kan inte ångras."):
                            delete_user(username)
                            st.success(f"Ditt konto, {username}, har tagits bort.")
                            st.stop()  # Stoppar vidare körning efter borttagning
            else:
                st.warning("Fel användarnamn eller lösenord")

    elif choice == "Registrera":
        st.subheader("Registrera ny användare")
        new_user = st.text_input("Användarnamn")
        new_password = st.text_input("Lösenord", type="password")

        if st.button("Registrera"):
            if new_user and new_password:
                try:
                    register_user(new_user, new_password)
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

                # Hämta användare från databasen
                users = get_users()
                for user in users:
                    st.write(f"{user[0]} - {'Admin' if user[1] else 'Användare'}")

                    # Ta bort användare
                    if st.button(f"Ta bort {user[0]}"):
                        delete_user(user[0])
                        st.success(f"{user[0]} har tagits bort")
                    
                    # Uppdatera användarroll
                    if user[0] != 'admin':
                        change_role = st.checkbox(f"Gör {user[0]} till admin" if not user[1] else f"Gör {user[0]} till användare")
                        if st.button(f"Uppdatera roll för {user[0]}"):
                            update_user_role(user[0], change_role)
                            st.success(f"Roll för {user[0]} uppdaterad")

if __name__ == '__main__':
    main()
