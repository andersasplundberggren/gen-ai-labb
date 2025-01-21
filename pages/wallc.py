import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data(region, gender, age_group, years):
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    query = {
        "query": [
            {"code": "Region", "selection": {"filter": "vs:RegionKommun07EjAggrB", "values": [region]}},
            {"code": "Kon", "selection": {"filter": "item", "values": [gender]}},
            {"code": "Alder", "selection": {"filter": "item", "values": [age_group]}},
            {"code": "Tid", "selection": {"filter": "item", "values": years}}
        ],
        "response": {"format": "json"}
    }
    response = requests.post(url, json=query)
    try:
        return response.json()
    except requests.JSONDecodeError:
        st.error(f"Failed to decode JSON. Status Code: {response.status_code}")
        st.text(response.text)  # Visa råsvaret för vidare diagnos
        return None

def process_data(response_data):
    if response_data and 'data' in response_data:
        data = []
        for item in response_data['data']:
            year = item['key'][3]
            value = item['values'][0]
            data.append({'År': year, 'Befolkning': value})
        return pd.DataFrame(data)
    else:
        return pd.DataFrame()

st.title("Befolkningsframskrivning för vald kommun och åldersgrupp")
region_val = st.text_input("Ange kommunkod", "1883")  # Exempel: Karlskoga Kommun
gender_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
age_group_val = st.selectbox("Välj åldersgrupp", ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100+"])
year_val = [str(year) for year in range(2024, 2031)]

if st.button("Hämta data"):
    response_data = fetch_data(region_val, gender_val, age_group_val, year_val)
    if response_data:
        df = process_data(response_data)
        if not df.empty:
            st.write(df)
            fig, ax = plt.subplots()
            ax.plot(df['År'], df['Befolkning'], marker='o')
            ax.set_title('Befolkningsutveckling')
            ax.set_xlabel('År')
            ax.set_ylabel('Befolkning')
            st.pyplot(fig)
        else:
            st.error("Ingen behandlingsbar data returnerades.")
    else:
        st.error("Ingen data returnerades från API.")
