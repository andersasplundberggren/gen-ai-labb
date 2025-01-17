import streamlit as st
import io
import contextlib
import traceback

# Titel för appen
st.set_page_config(page_title="Python Code Runner", layout="wide")
st.title("Python Code Runner")

# Layout med två kolumner
col1, col2 = st.columns(2)

with col1:
    st.subheader("Skriv din Python-kod här")
    code = st.text_area("", height=400, placeholder="# Skriv din kod här\nprint('Hello, World!')")

with col2:
    st.subheader("Output")
    output_area = st.empty()

# Kör koden när användaren trycker på en knapp
if st.button("Kör kod"):
    if code.strip():
        output_buffer = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code, {})
            output = output_buffer.getvalue()
        except Exception as e:
            output = traceback.format_exc()
        finally:
            output_buffer.close()

        output_area.code(output, language="plaintext")
    else:
        output_area.write("Ingen kod att köra. Skriv något i textrutan!")
