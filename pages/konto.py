import streamlit as st
import io
import contextlib
import traceback
import matplotlib.pyplot as plt
import numpy as np

# Titel för appen
st.set_page_config(page_title="Python Code Runner", layout="wide")
st.title("Python Code Runner")

# Layout med två kolumner
col1, col2 = st.columns(2)

with col1:
    st.subheader("Skriv din Python-kod här")
    code = st.text_area("", height=400, placeholder="# Skriv din kod här\nprint('Hello, World!')")

    st.subheader("Exempel på kod att testa:")
    examples = {
        "Skriva ut text": """# Exempel: Skriva ut text
print('Hej, världen!')""",
        "Loopar": """# Exempel: Loopar
for i in range(5):
    print(f'Räknar: {i}')""",
        "Funktioner": """# Exempel: Funktioner
def add(a, b):
    return a + b

result = add(3, 5)
print(f'Summan är: {result}')""",
        "Villkor": """# Exempel: Villkor
x = 10
y = 20
if x < y:
    print(f'{x} är mindre än {y}')
else:
    print(f'{x} är inte mindre än {y}')""",
        "Listor och iteration": """# Exempel: Listor och iteration
my_list = [1, 2, 3, 4, 5]
for num in my_list:
    print(f'Talet är: {num}')"""
    }

    selected_example = st.selectbox("Välj ett exempel", options=examples.keys())
    st.code(examples[selected_example], language="python")

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

# Sektion för att rita mönster
st.subheader("Rita mönster med Python")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Skriv din kod för att rita")
    pattern_code = st.text_area("", height=400, placeholder="# Skriv kod för att rita mönster\nimport matplotlib.pyplot as plt\n\nplt.plot([0, 1, 2, 3], [0, 1, 4, 9])\nplt.show()")

    st.subheader("Exempel på mönster:")
    pattern_examples = {
        "Rita en linje": """# Exempel: Rita en linje
import matplotlib.pyplot as plt

plt.plot([0, 1, 2, 3], [0, 1, 4, 9])
plt.title('Enkel linje')
plt.show()""",
        "Rita en cirkel": """# Exempel: Rita en cirkel
import matplotlib.pyplot as plt
import numpy as np

angles = np.linspace(0, 2 * np.pi, 100)
x = np.cos(angles)
y = np.sin(angles)

plt.plot(x, y)
plt.title('Enkel cirkel')
plt.axis('equal')
plt.show()""",
        "Rita flera linjer": """# Exempel: Rita flera linjer
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), label='sin(x)')
plt.plot(x, np.cos(x), label='cos(x)')
plt.title('Sinus och cosinus')
plt.legend()
plt.show()"""
    }

    selected_pattern = st.selectbox("Välj ett mönsterexempel", options=pattern_examples.keys())
    st.code(pattern_examples[selected_pattern], language="python")

with col4:
    st.subheader("Output för mönster")
    pattern_output = st.empty()

# Kör mönsterkoden när användaren trycker på en knapp
if st.button("Rita mönster"):
    if pattern_code.strip():
        pattern_buffer = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(pattern_buffer):
                exec(pattern_code, globals())
            output = pattern_buffer.getvalue()
            st.pyplot()
        except Exception as e:
            output = traceback.format_exc()
        finally:
            pattern_buffer.close()

        pattern_output.code(output, language="plaintext")
    else:
        pattern_output.write("Ingen kod att köra. Skriv något i textrutan!")
