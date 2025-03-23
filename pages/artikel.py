import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from openai import OpenAI
import os

# Sidotitel
st.title("Artikelsökare med nyckelord")

# Indata från användaren
st.subheader("Inställningar")
websites = st.text_area("Webbplatser att söka igenom (en URL per rad):", 
                       placeholder="https://example.com/\nhttps://another-site.com/")
keywords = st.text_area("Nyckelord att söka efter (separera med kommatecken):", 
                       placeholder="klimat, politik, ekonomi")
depth = st.slider("Sökdjup (antal nivåer av länkar att följa)", 1, 3, 1)

# Hämta OpenAI API-nyckel från Streamlit Secrets
# Notera: Detta förutsätter att du har lagt till din API-nyckel i Streamlit Secrets
client = None
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.warning("OpenAI API-nyckel hittades inte i Streamlit Secrets.")

def extract_article_content(url):
    """Hämtar och analyserar webbsidan för att extrahera artikelinnehåll"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Kontrollera om begäran lyckades
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ta bort script och style-element
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Hitta huvudartikeln (detta kan behöva anpassas för specifika webbplatser)
        article = soup.find('article')
        if not article:
            # Om ingen article-tagg hittades, försök med main
            article = soup.find('main')
        if not article:
            # Om ingen main-tagg hittades, använd body
            article = soup.body
            
        # Extrahera text från huvudelement
        if article:
            paragraphs = article.find_all('p')
            text = ' '.join([p.get_text().strip() for p in paragraphs])
            
            # Rensa upp texten
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Om texten är för kort, kan det hända att vi inte hittat innehållet
            if len(text) < 200 and article == soup.body:
                # Sista utvägen: ta all text från body
                text = soup.body.get_text(separator=' ', strip=True)
                text = re.sub(r'\s+', ' ', text).strip()
        else:
            text = ""
            
        # Försök hitta titel
        title = ""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.string
        if not title:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text().strip()
                
        return {'url': url, 'title': title, 'content': text}
    except Exception as e:
        st.error(f"Fel vid hämtning av {url}: {str(e)}")
        return {'url': url, 'title': f"HÄMTNINGSFEL: {str(e)}", 'content': ""}

def find_all_links(url, base_domain):
    """Hittar alla länkar på en webbsida som tillhör samma domän"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        # Kontrollera om begäran lyckades
        if response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        # Hitta alla <a>-taggar
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Normalisera URL:en
            if href.startswith('/'):
                # Relativ URL, lägg till basdomänen
                full_url = f"{base_domain.rstrip('/')}{href}"
            elif href.startswith('http'):
                # Absolut URL, kontrollera om den tillhör samma domän
                if not href.startswith(base_domain):
                    continue
                full_url = href
            else:
                # Ignorera andra URL-typer (t.ex. javascript:, mailto:)
                continue
                
            if full_url not in links:
                links.append(full_url)
                
        return links
    except Exception as e:
        st.warning(f"Kunde inte hämta länkar från {url}: {str(e)}")
        return []

def get_base_domain(url):
    """Extraherar basdomänen från en URL"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    # Matcha domän och protokoll
    match = re.match(r'(https?://[^/]+)', url)
    if match:
        return match.group(1)
    return url

def contains_keywords(text, keywords_list):
    """Kontrollerar om texten innehåller några av nyckelorden"""
    if not text:
        return False
    
    text_lower = text.lower()
    for keyword in keywords_list:
        if keyword.lower() in text_lower:
            return True
    return False

def analyze_with_ai(content, keywords_list):
    """Analyserar artikelinnehåll med OpenAI API för att få en sammanfattning"""
    if not client:
        return "OpenAI API inte tillgänglig"
    
    if not content or len(content) < 50:
        return "Otillräckligt innehåll för analys"
    
    try:
        # Förbereda prompt för GPT
        prompt = f"""
        Analysera följande artikelinnehåll:
        
        {content[:5000]}  # Begränsa längden för att undvika token-begränsningar
        
        1. Identifiera och nämn de nyckelord i listan som är relevanta för artikeln: {', '.join(keywords_list)}
        2. Ge en kort sammanfattning (max 3 meningar)
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en hjälpsam assistent som analyserar artikelinnehåll."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"AI-analys misslyckades: {str(e)}"

def crawl_website(start_url, keywords_list, max_depth=1):
    """Crawlar en webbplats till ett visst djup för att hitta artiklar med nyckelord"""
    base_domain = get_base_domain(start_url)
    visited_urls = set()
    urls_to_visit = [(start_url, 0)]  # (url, depth)
    matching_articles = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    i = 0
    total_urls = 1  # Börja med start-URL:en
    
    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0)
        
        # Undvik att besöka samma URL igen
        if current_url in visited_urls:
            continue
            
        # Markera URL:en som besökt
        visited_urls.add(current_url)
        
        # Uppdatera status
        i += 1
        progress = min(i / total_urls, 1.0) if total_urls > 0 else 0
        progress_bar.progress(progress)
        status_text.text(f"Analyserar URL {i}: {current_url}")
        
        # Hämta innehåll
        article_data = extract_article_content(current_url)
        
        # Kontrollera om artikeln innehåller nyckelorden
        if contains_keywords(article_data['content'], keywords_list):
            # Lägg till AI-analys om tillgänglig
            if client:
                article_data['ai_analysis'] = analyze_with_ai(article_data['content'], keywords_list)
            matching_articles.append(article_data)
            
        # Om vi inte har nått maxdjupet, lägg till fler URL:er att besöka
        if current_depth < max_depth:
            new_links = find_all_links(current_url, base_domain)
            
            # Lägg till nya länkar som inte har besökts ännu
            for link in new_links:
                if link not in visited_urls:
                    urls_to_visit.append((link, current_depth + 1))
                    total_urls += 1
                    
        # Uppdatera progress_bar med nya antalet URL:er
        progress = min(i / total_urls, 1.0) if total_urls > 0 else 0
        progress_bar.progress(progress)
        
        # Kort paus för att undvika att belasta servern
        time.sleep(0.5)
    
    # Rensa upp
    progress_bar.empty()
    status_text.empty()
    
    return matching_articles

# Huvudfunktion för webbsökning
if st.button("Sök efter artiklar"):
    if not websites or not keywords:
        st.error("Du måste ange minst en webbplats och ett nyckelord.")
    else:
        website_list = [line.strip() for line in websites.split('\n') if line.strip()]
        keyword_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        st.info(f"Söker igenom {len(website_list)} webbplatser efter {len(keyword_list)} nyckelord med djup {depth}...")
        
        all_results = []
        
        for website in website_list:
            st.subheader(f"Söker igenom: {website}")
            results = crawl_website(website, keyword_list, max_depth=depth)
            all_results.extend(results)
            
        if all_results:
            st.success(f"Hittade {len(all_results)} artiklar som matchar dina nyckelord!")
            
            # Visa resultaten i en tabell
            result_df = pd.DataFrame([{
                'Titel': r['title'], 
                'URL': r['url'], 
                'AI-analys': r.get('ai_analysis', 'Inte analyserad')
            } for r in all_results])
            
            st.dataframe(result_df)
            
            # Exportalternativ
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Ladda ner resultat som CSV",
                csv,
                "artikel_resultat.csv",
                "text/csv",
                key='download-csv'
            )
            
            # Detaljerad visning av varje artikel
            st.subheader("Detaljerade resultat")
            for i, article in enumerate(all_results):
                with st.expander(f"{article['title'][:60]}..."):
                    st.write(f"**URL:** {article['url']}")
                    st.write(f"**Titel:** {article['title']}")
                    st.write("**AI-analys:**")
                    st.write(article.get('ai_analysis', 'Inte analyserad'))
                    st.write("**Textutdrag:**")
                    st.text_area("", article['content'][:500] + "...", height=150, key=f"content_{i}")
        else:
            st.warning("Inga artiklar hittades som matchar dina nyckelord.")

# Information och instruktioner
with st.expander("Instruktioner och information"):
    st.markdown("""
    ### Hur du använder artikelsökaren
    
    1. **Webbplatser att söka igenom**: Ange en eller flera URL:er, en per rad.
    2. **Nyckelord**: Ange de nyckelord du vill söka efter, åtskilda med kommatecken.
    3. **Sökdjup**: Välj hur många nivåer av länkar som ska följas (högre värden tar längre tid).
    4. Klicka på **Sök efter artiklar** för att starta sökningen.
    
    ### Tips
    - Större djup ger fler resultat men tar längre tid att genomföra
    - Var specifik med dina nyckelord för att minska antalet irrelevanta träffar
    - För bästa resultat, använd fullständiga URL:er inklusive "https://"
    
    ### Begränsningar
    - Vissa webbplatser blockerar automatiserad insamling
    - Komplexa webbplatser med JavaScript-beroende innehåll kan ge oförutsägbara resultat
    - OpenAI API-användning kan medföra kostnader om du kör många sökningar
    """)
