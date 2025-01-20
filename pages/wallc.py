import streamlit as st
import pandas as pd
import requests
import json

# Titel och introduktion
st.title("PxWeb API: Statistikdata")
st.write("Den här appen hämtar data från PxWeb API och visar den i tabellformat.")

# JSON-frågan
json_query = {
    "query": [
        {
            "code": "Region",
            "selection": {
                "filter": "vs:RegionKommun07EjAggr",
                "values": ["1883"]
            }
        },
        {
            "code": "Kon",
            "selection": {
                "filter": "item",
                "values": ["1", "2", "1+2"]
            }
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
            }
        }
    ],
    "response": {"format": "json"}
}

# Ange API URL
api_url = st.text_input("Ange API URL", "http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0401/BE0401B/BefProgFoddaMedel11")

# Visa JSON-frågan
st.subheader("JSON-fråga")
st.json(json_query)

# Hämta data och visa tabell
if st.button("Hämta data"):
    try:
        response = requests.post(api_url, json=json_query)
        response.raise_for_status()  # Kontrollera om förfrågan lyckades
        data = response.json()

        # Extrahera data och visa som tabell
        columns = [col["text"] for col in data["columns"]]
        rows = [row["key"] + row["values"] for row in data["data"]]
        df = pd.DataFrame(rows, columns=columns + ["Value"])

        st.subheader("Statistikdata")
        st.dataframe(df)  # Interaktiv tabell

    except requests.exceptions.RequestException as e:
        st.error(f"Ett fel inträffade: {e}")
