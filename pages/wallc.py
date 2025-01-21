import streamlit as st
from pyscbwrapper import SCB
import pandas as pd
import matplotlib.pyplot as plt

# Inställa SCB-wrapper och sökväg till datan
scb = SCB('sv', 'BE', 'BE0401', 'BE0401A', 'BefProgRegFak')

def fetch_and_process_data(region, gender, age_group, years):
    scb.set_query(region=[region],
                  kon=[gender],
                  alder=[age_group],
                  tid=years)
    data = scb.get_data()
    df = pd.DataFrame(data['data'])
    df[['year', 'value']] = pd.DataFrame(df['key'].tolist(), index=df.index)
    df['value'] = pd.to_numeric(df['value'])
    df = df.pivot(index='year', values='value', columns='title')
    return df

def plot_data(df, title):
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    ax.set_title(title)
    ax.set_xlabel('År')
    ax.set_ylabel('Befolkning')
    st.pyplot(fig)

# Streamlit-gränssnitt
st.title("Befolkningsprognos")
gender_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
age_group_val = st.selectbox("Välj åldersgrupp", ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100+"])
region_val = "1883"  # Karlskoga kommunkod
year_val = [str(year) for year in range(2024, 2031)]

if st.button("Visa befolkningsutveckling"):
    df = fetch_and_process_data(region_val, gender_val, age_group_val, year_val)
    plot_data(df, 'Befolkningsutveckling i Karlskoga')
