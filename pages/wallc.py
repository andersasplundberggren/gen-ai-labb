import streamlit as st
import pandas as pd
from pyscbwrapper import SCB

# Initiera SCB-klienten
scb = SCB('sv', 'BE', 'BE0401', 'BE0401B', 'BefolkningNy')

# Hämta metadata för att få tillgängliga variabler
variables = scb.get_variables()

# Välj region
regions = scb.get_variable('Region')['values']
region = st.selectbox('Välj region:', regions)

# Välj kön
genders = scb.get_variable('Kon')['values']
gender = st.selectbox('Välj kön:', genders)

# Välj tidsperiod
years = scb.get_variable('Tid')['values']
start_year, end_year = st.select_slider(
    'Välj tidsperiod:',
    options=years,
    value=(years[0], years[-1])
)

# Skapa frågan
query = {
    'Region': [region],
    'Kon': [gender],
    'Tid': [str(year) for year in range(int(start_year), int(end_year) + 1)]
}

# Hämta data
data = scb.get_data(query)

# Omvandla data till DataFrame
df = pd.DataFrame(data['data'])

# Visa data i Streamlit
st.dataframe(df)
