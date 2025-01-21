import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

def fetch_data():
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    query = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "vs:RegionKommun07+",
                    "values": ["01883"]  # Exempelvärde för Karlskoga kommun
                }
            },
            {
                "code": "Kon",
                "selection": {
                    "filter": "item",
                    "values": ["1"]
                }
            },
            {
                "code": "Alder",
                "selection": {
                    "filter": "item",
                    "values": ["40-44"]
                }
            },
            {
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": ["2024"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Bad request ({response.status_code}): {response.text}")
        return None

def display_data(response_data):
    if response_data and 'data' in response_data:
        population = []
        for data in response_data['data']:
            year = data['key'][3]
            value = data['values'][0]
            population.append({'År': year, 'Befolkning': value})
        df = pd.DataFrame(population)
        return df
    return None

st.title("SCB Befolkningsdata")
if st.button('Hämta data'):
    data = fetch_data()
    if data:
        df = display_data(data)
        if df is not None:
            st.write(df)
            fig, ax = plt.subplots()
            ax.plot(df['År'], df['Befolkning'], marker='o')
            ax.set_xlabel('År')
            ax.set_ylabel('Befolkning')
            st.pyplot(fig)
        else:
            st.error("Ingen data kunde bearbetas.")
    else:
        st.error("Inga data hämtades.")
