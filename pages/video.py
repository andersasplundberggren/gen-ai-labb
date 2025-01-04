import streamlit as st
import yt_dlp
import os
import time

# Funktion för att ladda ner video från valfri länk
@st.cache_data
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get('title', 'video')
        filepath = f"{title}.mp4"
        ydl.download([url])
        return filepath

# Streamlit-gränssnitt
st.title("Videonedladdare för flera plattformar")

# Inputfält för valfri videolänk
video_url = st.text_input("Klistra in länk till video (YouTube, Instagram, Facebook, SVT Play, m.fl.)", "")

if video_url:
    st.write(f"Du har klistrat in länk: {video_url}")
    
    if st.button("Ladda ner video"):
        with st.spinner("Laddar ner video..."):
            try:
                # Ladda ner videon från den inmatade länken
                filepath = download_video(video_url)
                
                # Visa progressindikator
                st.success("Videon har laddats ner!")
                
                # Ge användaren möjlighet att ladda ner videon
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="Ladda ner video",
                        data=file,
                        file_name=os.path.basename(filepath),
                        mime="video/mp4"
                    )
                
                # Rensa den nedladdade filen
                os.remove(filepath)
                
            except Exception as e:
                st.error(f"Ett fel inträffade: {e}")
