import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Funktion för att hämta data från SCB API för Karlskoga kommun
def fetch_data(age_range, num_years):
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    query = {
        "query": [
            {"code": "Region", "selection": {"filter": "vs:RegionKommun07EjAggrB", "values": ["1883"]}},  # Karlskoga
            {"code": "Alder", "selection": {"filter": "item", "values": [age_range]}},
            {"code": "Tid", "selection": {"filter": "top", "values": [num_years]}}
        ],
        "response": {"format": "json"}
    }
    response = requests.post(url, json=query)
    if response.status_code != 200:
        st.error("Failed to fetch data")
        return pd.DataFrame()
    return pd.DataFrame([
        {'Year': item['key'][2], 'Population': item['values'][0]}
        for item in response.json()['data']
    ])

# Streamlit UI
st.title('Karlskoga Kommun Befolkningsdata')

age_range = st.selectbox("Välj åldersgrupp", options=[
    "0-4", "5-9", "10-14", "15-19", "20-24", "25-29",
    "30-34", "35-39", "40-44", "45-49", "50-54",
    "55-59", "60-64", "65-69", "70-74", "75-79",
    "80-84", "85-89", "90+"
], index=4)  # default to "20-24"

num_years = st.slider("Antal senaste år att visa", min_value=1, max_value=10, value=5)

if st.button('Ladda data och visa diagram'):
    df = fetch_data(age_range, str(num_years))
    if not df.empty:
        fig, ax = plt.subplots()
        ax.plot(df['Year'], df['Population'], marker='o')
        ax.set_title(f'Population trends for age {age_range}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population')
        st.pyplot(fig)
    else:
        st.write("Ingen data tillgänglig. Kontrollera valda parametrar.")
