import streamlit as st

# Inbäddad JSON-struktur
json_data = {
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
        }
    ]
}

# Huvudapplikation
def main():
    st.title("Inbäddad JSON-struktur")
    st.json(json_data)  # Visar JSON-strukturen i Streamlit-applikationen

if __name__ == "__main__":
    main()
