import streamlit as st
import json

# Ursprunglig JSON-struktur
default_json = {
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
    st.title("Hantera JSON-struktur i Streamlit")

    # Visa JSON-strukturen
    st.subheader("Ursprunglig JSON-struktur")
    st.json(default_json)

    # Låter användaren redigera JSON-strukturen
    st.subheader("Redigera JSON-strukturen")
    json_input = st.text_area("Redigera JSON här:", value=json.dumps(default_json, indent=4))
    
    # Försök att tolka användarens inmatning som JSON
    try:
        edited_json = json.loads(json_input)
        st.success("JSON-strukturen är giltig!")
        st.subheader("Redigerad JSON-struktur")
        st.json(edited_json)
    except json.JSONDecodeError:
        st.error("Ogiltig JSON! Kontrollera formatet och försök igen.")

if __name__ == "__main__":
    main()
