import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

def fetch_data(years, gender, age_group):
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    gender_text = "kvinnor" if gender == "2" else "män"
    age_text = f"{age_group}"
    query = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "vs:RegionKommun07EjAggrB",
                    "values": ["1883"]
                }
            },
            {
                "code": "Kon",
                "selection": {
                    "filter": "item",
                    "values": [gender]
                }
            },
            {
                "code": "Alder",
                "selection": {
                    "filter": "item",
                    "values": [age_group]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    if response.status_code == 200:
        try:
            data = response.json()
            st.write("DEBUG: ", data)  # Lägger till en debug-utskrift för att se datan
            return data
        except requests.exceptions.JSONDecodeError:
            st.error("Kunde inte tolka svaret som JSON. Här är råsvaret: {}".format(response.text))
            return None
    else:
        st.error(f"Kunde inte hämta data från SCB. Statuskod: {response.status_code}")
        return None

def process_data(response_data):
    # Tänkt att fyllas i när vi sett strukturen på JSON-svaret
    pass

def plot_data(df):
    fig, ax = plt.subplots()
    ax.plot(df['År'], df['Befolkning'])
    ax.set_title('Befolkningsutveckling')
    ax.set_xlabel('År')
    ax.set_ylabel('Befolkning')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Användargränssnitt
st.title("Befolkningsdata för Karlskoga")
gender_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
age_group_val = st.selectbox("Välj åldersgrupp", ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100+"])
year_val = st.multiselect("Välj år", [str(year) for year in range(2024, 2071)], default=[str(year) for year in range(2024, 2031)])

if st.button("Visa befolkningsutveckling"):
    response_data = fetch_data(year_val, gender_val, age_group_val)

# Efter att ha sett JSON-strukturen, kommer vi att kunna skriva process_data korrekt
