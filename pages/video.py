import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Funktion för att hämta data från SCB API
def fetch_data(år, kön, ålder):
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    query = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "vs:RegionKommun07EjAggrB",
                    "values": ["1883"]  # Karlskoga kommunkod
                }
            },
            {
                "code": "InrikesUtrikes",
                "selection": {
                    "filter": "item",
                    "values": ["13", "23", "83"]
                }
            },
            {
                "code": "Kon",
                "selection": {
                    "filter": "item",
                    "values": [kön]
                }
            },
            {
                "code": "Alder",
                "selection": {
                    "filter": "agg:Ålder10årJ",
                    "values": [ålder]
                }
            }
        ],
        "response": {
            "format": "px"
        }
    }

    response = requests.post(url, json=query)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Kunde inte hämta data från SCB.")
        return None

# Funktion för att bearbeta och formatera data
def process_data(response_data):
    if not response_data:
        return None
    
    # Här antar vi att data kommer i ett format med tabellvärden i "Data"
    data_values = response_data.get("data", [])

    # Extrahera relevant information från svaret
    years = [int(year) for year in response_data.get("header", {}).get("values", [])]
    population_values = [float(value) for value in data_values]

    # Skapa en DataFrame för att underlätta hantering
    df = pd.DataFrame({
        'År': years,
        'Befolkning': population_values
    })
    
    # Avrunda till heltal
    df['Befolkning'] = df['Befolkning'].round().astype(int)
    return df

# Funktion för att visa diagram
def plot_data(df):
    fig, ax = plt.subplots()
    ax.plot(df['År'], df['Befolkning'], marker='o')
    ax.set_title('Befolkningsutveckling i Karlskoga')
    ax.set_xlabel('År')
    ax.set_ylabel('Befolkning')
    st.pyplot(fig)

# Streamlit-gränssnitt
st.title("Befolkningsframskrivning för Karlskoga kommun")

# Användarens urval
kön_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
ålder_val = st.selectbox("Välj åldersgrupp", ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-99", "100+"])
år_val = st.multiselect("Välj år", [str(year) for year in range(2024, 2071)], default=[str(year) for year in range(2024, 2031)])

# När användaren har gjort sitt urval, hämta och visa data
if st.button("Visa befolkningsutveckling"):
    response_data = fetch_data(år_val, kön_val, ålder_val)
    df = process_data(response_data)
    if df is not None:
        st.write(f"Visar data för {ålder_val} år, {kön_val} under åren {', '.join(år_val)}.")
        plot_data(df)
