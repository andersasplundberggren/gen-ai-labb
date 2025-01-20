import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# Testdata
data = {
    'År': [2024, 2025, 2026, 2027, 2028],
    'Befolkning': [1724, 1702, 1690, 1680, 1670]
}

df = pd.DataFrame(data)

# Skapa diagram
fig, ax = plt.subplots()
ax.plot(df['År'], df['Befolkning'])
ax.set_title('Testdiagram')
ax.set_xlabel('År')
ax.set_ylabel('Befolkning')

# Visa diagram i Streamlit
st.pyplot(fig)
