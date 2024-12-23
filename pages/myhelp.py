import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# OpenAI API
client = OpenAI(api_key="YOUR_API_KEY")

# Scraping-funktion
def fetch_articles(url, keywords):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = soup.find_all('article')  # Anpassa efter sidan
    filtered_articles = []

    for article in articles:
        text = article.get_text()
        if any(keyword.lower() in text.lower() for keyword in keywords):
            link = article.find('a')['href']
            filtered_articles.append((text, link))
    
    return filtered_articles

# Sammanfattningsfunktion
def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the following article."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# E-postutskick
def send_email(summary, link):
    msg = MIMEText(f"{summary}\n\nLäs mer: {link}")
    msg['Subject'] = 'Automatisk Artikelsammanfattning'
    msg['From'] = "din.epost@exempel.com"
    msg['To'] = "mottagare@exempel.com"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login("din.epost@exempel.com", "LÖSENORD")
        server.send_message(msg)

# Streamlit-gränssnitt
st.title("Artikelbevakning och Sammanfattning")

url = st.text_input("Webbadress till sida att bevaka:")
keywords = st.text_area("Ange sökord (kommaseparerade):").split(',')

if st.button("Hämta Artiklar"):
    articles = fetch_articles(url, keywords)
    
    if articles:
        for text, link in articles:
            summary = summarize_text(text)
            st.write(summary)
            st.markdown(f"[Läs hela artikeln]({link})")
            send_email(summary, link)
    else:
        st.write("Inga artiklar hittades med de angivna sökorden.")

# Automatiserad schemaläggning
def job():
    fetch_articles(url, keywords)

schedule.every().day.at("09:00").do(job)
