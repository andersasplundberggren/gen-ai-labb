import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Funktion för att hämta data från SCB API
def fetch_data(years, gender, age_group):
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
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": years
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
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Kunde inte tolka svaret som JSON. Här är råsvaret: {}".format(response.text))
            return None
    else:
        st.error(f"Kunde inte hämta data från SCB. Statuskod: {response.status_code}")
        return None

# Funktion för att bearbeta och formatera data
def process_data(response_data):
    try:
        data = response_data['data']
        df = pd.DataFrame(data)
        # Antagande är att relevant data finns i columns 'key' och 'values'
        df['key'] = df['key'].apply(lambda x: x[2])  # år
        df['values'] = df['values'].astype(float)
        df.columns = ['År', 'Befolkning']
        df.set_index('År', inplace=True)
        return df
    except Exception as e:
        st.error(f"Ett fel uppstod när datan skulle bearbetas: {e}")
        return pd.DataFrame()

# Funktion för att visa diagram
def plot_data(df, gender, age_group):
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Befolkning'], marker='o')
    ax.set_title(f'Befolkningsutveckling i Karlskoga för {gender}, åldersgrupp {age_group}')
    ax.set_xlabel('År')
    ax.set_ylabel('Befolkning')
    st.pyplot(fig)

# Streamlit-gränssnitt
st.title("Befolkningsframskrivning för Karlskoga kommun")

# Användarens urval
gender_val = st.selectbox("Välj kön", ["1", "2"], format_func=lambda x: "Män" if x == "1" else "Kvinnor")
age_group_val = st.selectbox("Välj åldersgrupp", ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"])
year_val = st.multiselect("Välj år", [str(year) for year in range(2024, 2071)], default=[str(year) for year in range(2024, 2031)])

# När användaren har gjort sitt urval, hämta och visa data
if st.button("Visa befolkningsutveckling"):
    response_data = fetch_data(year_val, gender_val, age_group_val)
    df = process_data(response_data)
    if not df.empty:
        st.write(f"Visar data för åldersgrupp {age_group_val}, kön {gender_val}, under åren {', '.join(year_val)}.")
        plot_data(df, gender_val, age_group_val)
