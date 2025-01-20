import streamlit as st
import requests
import pandas as pd

# Titel
st.title("SCB Dataurval och Rapport")

# Urvalsfunktioner
region = st.selectbox("Välj region", ["1883", "1884"])  # Lägg till fler regioner
inrikes_utrikes = st.multiselect("Inrikes/Utrikes", ["13", "23", "83"])
kon = st.multiselect("Kön", ["1", "2"])
alder = st.multiselect("Ålder", ["-9", "10-19", "20-29", "30-39", "40-49", 
                                  "50-59", "60-69", "70-79", "80-89", "90-99", "100+"])

# API-fråga
if st.button("Hämta data"):
    payload = {
        "query": [
            {"code": "Region", "selection": {"filter": "vs:RegionKommun07EjAggrB", "values": [region]}},
            {"code": "InrikesUtrikes", "selection": {"filter": "item", "values": inrikes_utrikes}},
            {"code": "Kon", "selection": {"filter": "item", "values": kon}},
            {"code": "Alder", "selection": {"filter": "agg:Ålder10årJ", "values": alder}}
        ],
        "response": {"format": "px"}
    }
    
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['data'])  # Bearbeta JSON-svaret till tabell
        st.write(df)
        
        # Exportera till Excel
        st.download_button("Ladda ner som Excel", df.to_csv(index=False), file_name="rapport.csv")
    else:
        st.error("Kunde inte hämta data. Kontrollera urvalet.")
