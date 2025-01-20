import streamlit as st
import json

# JSON-data
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
        },
        {
            "code": "Tid",
            "selection": {
                "filter": "item",
                "values": ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
            }
        }
    ],
    "response": {
        "format": "px"
    }
}

# Webbappens layout
st.title("JSON-kod för publicering")
st.write("Här är JSON-koden som du angav:")

# Visa JSON-koden snyggt formaterad
st.json(json_data)

# Möjlighet att visa rå JSON-kod
st.subheader("Rå JSON-kod")
st.code(json.dumps(json_data, indent=4), language='json')

# Slut på appen
st.write("Du kan kopiera eller använda denna JSON-kod som referens!")
