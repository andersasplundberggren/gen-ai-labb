import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Titel
st.title("SCB Dataurval och Rapport - Karlskoga Kommun")

# Information om datan
st.markdown("**Observera:** Den här datan gäller enbart **Karlskoga kommun**.")

# Urvalsfunktioner
st.sidebar.header("Gör ditt urval")

inrikes_utrikes_val = {
    "13": "Inrikes födda",
    "23": "Utrikes födda",
    "83": "Totalt"
}
inrikes_utrikes = st.sidebar.multiselect("Inrikes/Utrikes", options=inrikes_utrikes_val.keys(), 
                                         format_func=lambda x: inrikes_utrikes_val[x])

kon_val = {
    "1": "Män",
    "2": "Kvinnor"
}
kon = st.sidebar.multiselect("Kön", options=kon_val.keys(), format_func=lambda x: kon_val[x])

alder = st.sidebar.multiselect("Ålder", options=["-9", "10-19", "20-29", "30-39", "40-49", 
                                                  "50-59", "60-69", "70-79", "80-89", "90-99", "100+"],
                                default=["10-19", "20-29", "30-39"])

# API-förfrågan
if st.sidebar.button("Hämta data"):
    payload = {
        "query": [
            {"code": "Region", "selection": {"filter": "vs:RegionKommun07EjAggrB", "values": ["1883"]}},  # Karlskoga kommun
            {"code": "InrikesUtrikes", "selection": {"filter": "item", "values": inrikes_utrikes}},
            {"code": "Kon", "selection": {"filter": "item", "values": kon}},
            {"code": "Alder", "selection": {"filter": "agg:Ålder10årJ", "values": alder}}
        ],
        "response": {"format": "px"}
    }
    
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # Konvertera data till DataFrame
        data = response.json()
        df = pd.DataFrame(data['data'])  # Anpassa efter hur svaret ser ut
        st.success("Data hämtades framgångsrikt!")
        
        # Visa data som tabell
        st.write("### Tabell över resultat")
        st.dataframe(df)
        
        # Generera graf
        st.write("### Visualisering av data")
        fig, ax = plt.subplots()
        df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Konvertera till numeriskt
        df.groupby('region')['value'].sum().plot(kind='bar', ax=ax)
        ax.set_title("Fördelning av värden för Karlskoga kommun")
        st.pyplot(fig)
        
        # Ladda ner data som CSV
        st.download_button("Ladda ner som CSV", df.to_csv(index=False), file_name="rapport.csv")
        
        # Ladda ner data som PDF (enkel lösning med HTML)
        import pdfkit
        html = df.to_html(index=False)
        pdf = pdfkit.from_string(html, False)
        st.download_button("Ladda ner som PDF", data=pdf, file_name="rapport.pdf", mime="application/pdf")
    else:
        st.error(f"Misslyckades med att hämta data. Felkod: {response.status_code}")
