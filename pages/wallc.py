import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

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
        "response": {"format": "csv"}
    }
    
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/BE/BE0401/BE0401A/BefProgRegFakN"
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        try:
            # Läs in CSV-data
            data_text = response.text
            data = StringIO(data_text)
            df = pd.read_csv(data, sep=";")  # Anpassa separator om nödvändigt
            st.success("Data hämtades framgångsrikt!")
            
            # Avrunda värden till heltal
            df['value'] = df['value'].round(0).astype(int)

            # Bearbeta och visualisera datan
            st.write("### Tabell över resultat")
            st.dataframe(df)

            # Här kan vi gruppera efter olika variabler (ex. kön eller ålder)
            st.write("### Visualisering av data")
            
            # Gruppera och summera per år och kön (kan även göras för ålder eller inrikes/utrikes)
            if 'Kon' in df.columns:
                df_grouped = df.groupby(['Tid', 'Kon'])['value'].sum().reset_index()
                df_grouped['Kon'] = df_grouped['Kon'].map(kon_val)  # Gör kön mer läsbart

                # Skapa grafen
                fig, ax = plt.subplots()
                for key, grp in df_grouped.groupby('Kon'):
                    ax.plot(grp['Tid'], grp['value'], label=key)

                ax.set_title("Befolkningsutveckling i Karlskoga kommun efter kön")
                ax.set_xlabel("År")
                ax.set_ylabel("Befolkningsantal")
                ax.legend(title='Kön')
                st.pyplot(fig)

            # Om du vill kan du även lägga till en graf för ålder
            elif 'Alder' in df.columns:
                df_grouped = df.groupby(['Tid', 'Alder'])['value'].sum().reset_index()
                
                # Skapa grafen
                fig, ax = plt.subplots()
                for key, grp in df_grouped.groupby('Alder'):
                    ax.plot(grp['Tid'], grp['value'], label=key)

                ax.set_title("Befolkningsutveckling i Karlskoga kommun efter ålder")
                ax.set_xlabel("År")
                ax.set_ylabel("Befolkningsantal")
                ax.legend(title='Ålder')
                st.pyplot(fig)

            # Ladda ner data som CSV
            st.download_button("Ladda ner som CSV", df.to_csv(index=False), file_name="rapport.csv")
            
            # Ladda ner data som PDF (enkel lösning med HTML)
            import pdfkit
            html = df.to_html(index=False)
            pdf = pdfkit.from_string(html, False)
            st.download_button("Ladda ner som PDF", data=pdf, file_name="rapport.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Kunde inte läsa och bearbeta API-svaret. Fel: {str(e)}")
            st.write("Svar från API:", response.text)  # Visa raw text från API-svaret
    else:
        st.error(f"Misslyckades med att hämta data. Felkod: {response.status_code}")
        st.write("Svar från API:", response.text)  # Visa raw text från API-svaret
