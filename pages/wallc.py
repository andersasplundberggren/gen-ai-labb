import streamlit as st
import pandas as pd
import requests

# Funktion för att hämta data från PxWeb API
def fetch_data(api_url, query):
    response = requests.post(api_url, json=query)
    response.raise_for_status()
    return response.json()

# Funktion för att omvandla API-svaret till en DataFrame
def process_data(data):
    variables = data['variables']
    col_names = [var['text'] for var in variables]
    values = data['data']
    records = [val['values'] for val in values]
    df = pd.DataFrame(records, columns=col_names)
    return df

# Streamlit-appens layout
st.title("Interaktiv Statistikvisning med PxWeb API")

# Ange API URL
api_url = st.text_input("Ange API URL", "http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0401/BE0401B/BefProgFoddaMedel11")

# Välj år
start_year, end_year = st.select_slider(
    'Välj tidsperiod:',
    options=[str(year) for year in range(2014, 2024)],
    value=('2014', '2023')
)

# Visa valda år
st.write(f"Vald period: {start_year} till {end_year}")

# Definiera JSON-frågan baserat på användarens val
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
                "values": [str(year) for year in range(int(start_year), int(end_year) + 1)]
            }
        }
    ],
    "response": {"format": "json"}
}

# Hämta och visa data när användaren klickar på knappen
if st.button("Hämta data"):
    try:
        data = fetch_data(api_url, json_query)
        df = process_data(data)
        st.subheader("Resultat")
        st.dataframe(df)
    except requests.exceptions.RequestException as e:
        st.error(f"Ett fel inträffade vid hämtning av data: {e}")
    except Exception as e:
        st.error(f"Ett oväntat fel inträffade: {e}")
