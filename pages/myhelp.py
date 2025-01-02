import streamlit as st
import requests
import openai
import re

# OpenAI API-nyckel
openai.api_key = st.secrets["openai_api_key"]

# Funktion för att söka efter artiklar

def search_articles(urls, keywords):
    results = {}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content = response.text
                found = []
                for keyword in keywords:
                    if re.search(rf'\b{keyword}\b', content, re.IGNORECASE):
                        found.append(keyword)
                if found:
                    results[url] = found
        except Exception as e:
            st.error(f"Error accessing {url}: {str(e)}")
    return results

# Streamlit gränssnitt
st.title("Automatisk Artikel-Sökning med OpenAI API")

urls = st.text_area("Ange webbadresser (en per rad)").split("\n")
keywords = st.text_area("Ange nyckelord (kommaseparerade)").split(",")

if st.button("Sök efter artiklar"):
    with st.spinner("Söker..."):
        results = search_articles(urls, keywords)
        if results:
            st.success("Artiklar hittade!")
            for url, words in results.items():
                st.write(f"**{url}** innehåller nyckelord: {', '.join(words)}")
        else:
            st.warning("Inga artiklar med dessa nyckelord hittades.")
