import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import schedule
import threading
import re
import nltk
from nltk.tokenize import sent_tokenize
import json
import os

# Ladda ner nödvändiga NLTK-data första gången
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Filnamn för datalagring
DATA_FILE = "articles_data.json"
CONFIG_FILE = "config.json"

# Standardkonfiguration
default_config = {
    "sources": [
        {"url": "https://www.example.com", "keywords": ["tech", "ai"]},
        {"url": "https://www.example2.com", "keywords": ["data", "streamlit"]}
    ],
    "scan_interval_days": 1,
    "last_scan": None
}

# Funktion för att ladda konfiguration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return default_config

# Funktion för att spara konfiguration
def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

# Funktion för att ladda artikel-data
def load_articles():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Funktion för att spara artikel-data
def save_articles(articles):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

# Funktion för att generera en kort sammanfattning av artikeltext
def generate_summary(text, max_sentences=3):
    if not text:
        return "Ingen text tillgänglig för sammanfattning."
    
    # Dela upp texten i meningar
    sentences = sent_tokenize(text)
    
    # Begränsa till max_sentences eller färre
    if len(sentences) <= max_sentences:
        return " ".join(sentences)
    
    # Enkel sammanfattning - ta de första meningarna
    return " ".join(sentences[:max_sentences]) + "..."

# Funktion för att hämta artiklar från en URL
def fetch_articles(url, keywords):
    articles = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Hitta alla länkar
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            text = link.text.strip()
            
            # Kontrollera om länken är relevant (innehåller något av nyckelorden)
            if href and any(keyword.lower() in text.lower() or keyword.lower() in href.lower() for keyword in keywords):
                # Normalisera URL:er
                if href.startswith('/'):
                    base_url = '/'.join(url.split('/')[:3])  # http(s)://domain.com
                    href = base_url + href
                
                # Hämta artikel-innehållet
                try:
                    article_response = requests.get(href, headers=headers, timeout=10)
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    
                    # Försök hitta huvudinnehållet (p-taggar)
                    paragraphs = article_soup.find_all('p')
                    content = ' '.join([p.text for p in paragraphs])
                    
                    # Skapa en sammanfattning
                    summary = generate_summary(content)
                    
                    # Försök hitta en titel
                    title = article_soup.title.text if article_soup.title else text
                    
                    # Skapa artikel-objekt
                    article = {
                        "title": title,
                        "url": href,
                        "summary": summary,
                        "source": url,
                        "found_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "keywords": [keyword for keyword in keywords if keyword.lower() in text.lower() or keyword.lower() in href.lower()]
                    }
                    
                    articles.append(article)
                except Exception as e:
                    print(f"Kunde inte bearbeta artikel {href}: {str(e)}")
    
    except Exception as e:
        print(f"Fel vid hämtning från {url}: {str(e)}")
    
    return articles

# Funktion för att köra en fullständig scan
def run_scan():
    config = load_config()
    existing_articles = load_articles()
    
    # Skapa en uppslagning av befintliga URL:er för att undvika dubletter
    existing_urls = {article["url"] for article in existing_articles}
    
    new_articles = []
    
    for source in config["sources"]:
        url = source["url"]
        keywords = source["keywords"]
        
        print(f"Skannar {url} efter nyckelorden {keywords}...")
        articles = fetch_articles(url, keywords)
        
        # Lägg till nya artiklar
        for article in articles:
            if article["url"] not in existing_urls:
                new_articles.append(article)
                existing_urls.add(article["url"])
    
    # Uppdatera och spara
    if new_articles:
        all_articles = new_articles + existing_articles
        # Sortera efter hittad-datum, nyast först
        all_articles.sort(key=lambda x: x["found_date"], reverse=True)
        save_articles(all_articles)
        print(f"Hittade {len(new_articles)} nya artiklar.")
    else:
        print("Inga nya artiklar hittades.")
    
    # Uppdatera tidpunkten för senaste sökningen
    config["last_scan"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_config(config)

# Funktion för att köra schemalagda skanningar i bakgrunden
def schedule_scanner():
    config = load_config()
    interval_days = config["scan_interval_days"]
    
    def job():
        print(f"Kör schemalagd skanning...")
        run_scan()
    
    # Kör en initial scan
    job()
    
    # Schemalägg regelbundna skannningar
    schedule.every(interval_days).days.at("00:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Kontrollera varje minut

# Starta en bakgrundstråd för skanning
def start_background_thread():
    thread = threading.Thread(target=schedule_scanner, daemon=True)
    thread.start()

# Admin-sidan
def admin_page():
    st.title("Admin - Artikelaggregator Konfiguration")
    
    config = load_config()
    
    st.header("Källor och Nyckelord")
    
    sources = config["sources"]
    updated_sources = []
    
    for i, source in enumerate(sources):
        st.subheader(f"Källa {i+1}")
        col1, col2 = st.columns(2)
        
        with col1:
            url = st.text_input(f"URL {i+1}", value=source["url"], key=f"url_{i}")
        with col2:
            keywords_str = st.text_input(f"Nyckelord {i+1} (kommaseparerade)", 
                                        value=", ".join(source["keywords"]), 
                                        key=f"keywords_{i}")
        
        keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
        updated_sources.append({"url": url, "keywords": keywords})
        
        if st.button(f"Ta bort källa {i+1}", key=f"remove_{i}"):
            continue
    
    if st.button("Lägg till ny källa"):
        updated_sources.append({"url": "", "keywords": []})
    
    # Filtrera bort tomma källor
    config["sources"] = [s for s in updated_sources if s["url"]]
    
    st.header("Inställningar")
    config["scan_interval_days"] = st.number_input(
        "Intervall för skanning (dagar)", 
        min_value=1, 
        value=config["scan_interval_days"],
        step=1
    )
    
    if st.button("Spara konfiguration"):
        save_config(config)
        st.success("Konfigurationen har sparats!")
    
    if st.button("Kör skanning nu"):
        with st.spinner("Skannar källor..."):
            run_scan()
        st.success("Skanning slutförd!")
    
    st.header("Befintliga Artiklar")
    articles = load_articles()
    
    if articles:
        st.write(f"Totalt antal artiklar: {len(articles)}")
        
        if st.button("Rensa alla artiklar"):
            save_articles([])
            st.success("Alla artiklar har rensats!")
            st.experimental_rerun()
    else:
        st.info("Inga artiklar hittade än.")

# Besökarsidan
def visitor_page():
    st.title("Artikelsammanfattningar")
    
    articles = load_articles()
    
    if not articles:
        st.info("Inga artiklar hittade än. Kom tillbaka senare!")
        return
    
    # Filter för nyckelord
    all_keywords = set()
    for article in articles:
        all_keywords.update(article.get("keywords", []))
    
    if all_keywords:
        selected_keywords = st.multiselect(
            "Filtrera efter nyckelord:", 
            list(all_keywords)
        )
    
    # Visa artiklar
    for article in articles:
        # Filtrera efter valda nyckelord om något är valt
        if selected_keywords and not any(keyword in article.get("keywords", []) for keyword in selected_keywords):
            continue
            
        st.subheader(article["title"])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**Källa:** {article['source']}")
            st.markdown(f"**Hittad:** {article['found_date']}")
        with col2:
            st.markdown(f"[Läs original]({article['url']})")
            
        with st.expander("Visa sammanfattning"):
            st.write(article["summary"])
        
        st.markdown("---")

# Huvudfunktion
def main():
    st.sidebar.title("Navigation")
    
    # Enkel autentisering för admin (i verkligheten skulle du använda något säkrare)
    is_admin = False
    if st.sidebar.checkbox("Admin-läge"):
        admin_password = st.sidebar.text_input("Lösenord", type="password")
        if admin_password == "admin":  # Byt till ett säkrare lösenord
            is_admin = True
        else:
            st.sidebar.error("Felaktigt lösenord")
    
    if is_admin:
        admin_page()
    else:
        visitor_page()

if __name__ == "__main__":
    main()
    
    # Kontrollera om vi kör i Streamlit-miljö eller direkt
    import sys
    if not hasattr(st, '_is_running'):
        # Om vi kör direkt (inte via streamlit run)
        # Starta bakgrundstråden för skanning
        start_background_thread()
