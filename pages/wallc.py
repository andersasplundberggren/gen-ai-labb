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
    
    if response.status_code == 200:
        try:
            return response.json()
        except requests.JSONDecodeError:
            st.error(f"Failed to decode JSON. Response body: {response.text}")
            return None
    else:
        st.error(f"Bad request ({response.status_code}): {response.text}")
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
region_val = st.text_input("Ange kommunkod", "1883")
gender_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
age_group_val = "20-24"  # Använda ett fixt värde tillfälligt 
year_val = ["2024", "2025"]  # Använda ett begränsat antal år tillfälligt

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
            st.error("Ingen processbar data returnerades.")
    else:
        st.error("Misslyckades med att hämta data från SCB.")
