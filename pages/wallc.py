import requests

def fetch_data():
    url = "http://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0401/BE0401B/BefProgFoddaMedel11"
    query = {
        "query": [
            {"code": "Fodelseland", "selection": {"filter": "item", "values": ["010", "020"]}},
            {"code": "Alder", "selection": {"filter": "item", "values": ["15-64"]}},
            {"code": "Tid", "selection": {"filter": "top", "values": ["10"]}}
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

data = fetch_data()
if data:
    print(data)
