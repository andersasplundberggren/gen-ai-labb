import streamlit as st
import requests
import openai
import re

# OpenAI API-nyckel
openai.api_key = st.secrets[""]

# Funktion för att söka efter artiklar och sammanfatta dem

def search_and_summarize_articles(urls, keywords):
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
                    results[url] = {
                        'keywords': found,
                        'summary': summarize_article(content),
                        'link': url
                    }
        except Exception as e:
            st.error(f"Error accessing {url}: {str(e)}")
    return results

# Funktion för att sammanfatta artiklar med OpenAI API
def summarize_article(content):
    prompt = f"Sammanfatta följande text:\n{content[:2000]}"  # Begränsar till 4000 tecken
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sammanfattning misslyckades: {str(e)}"

# Streamlit gränssnitt
st.title("Automatisk Artikel-Sökning och Sammanfattning med OpenAI API")

urls = st.text_area("Ange webbadresser (en per rad)").split("\n")
keywords = st.text_area("Ange nyckelord (kommaseparerade)").split(",")

if st.button("Sök och Sammanfatta Artiklar"):
    with st.spinner("Söker och sammanfattar..."):
        results = search_and_summarize_articles(urls, keywords)
        if results:
            st.success("Artiklar hittade och sammanfattade!")
            for url, data in results.items():
                st.write(f"**[{url}]({url})** innehåller nyckelord: {', '.join(data['keywords'])}")
                st.write(f"**Sammanfattning:** {data['summary']}")
        else:
            st.warning("Inga artiklar med dessa nyckelord hittades.")
