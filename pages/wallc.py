import streamlit as st
import plotly.express as px
import pandas as pd

# Skapa en grundläggande tidslinje med exempeldata
def skapa_tidslinje():
    # Exempeldata för tidslinjen
    data = {
        'Tidpunkt': ['2025-01-01', '2025-01-10', '2025-01-15', '2025-01-20'],
        'Händelse': ['Introduktion', 'Diskussion 1', 'Gruppövning', 'Avslutning'],
        'Beskrivning': ['Introduktion till workshopen', 'Första diskussionen om ämnet', 'Grupparbete och samarbete', 'Sammanfattning och avslutning']
    }

    df = pd.DataFrame(data)
    df['Tidpunkt'] = pd.to_datetime(df['Tidpunkt'])

    # Skapa tidslinje med Plotly
    fig = px.timeline(df, x_start="Tidpunkt", x_end="Tidpunkt", y="Händelse", title="Workshop Tidslinje",
                       hover_data=["Beskrivning"])

    # Visa tidslinjen
    st.plotly_chart(fig)

# Grundstruktur för Streamlit-appen
def main():
    st.title("Workshop Tidslinje")

    # Visa tidslinjen
    skapa_tidslinje()

    # Lägg till andra funktioner här i framtiden
    st.write("Fler funktioner kan läggas till här, som omröstningar eller interaktiva övningar.")

if __name__ == "__main__":
    main()
