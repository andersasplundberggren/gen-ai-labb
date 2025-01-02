import streamlit as st
from pytube import Search
import yt_dlp
import tempfile
import os

# Funktion som söker efter videor på YouTube utan API-nyckel
def search_youtube(query, max_results=3):
    search = Search(query)
    videos = search.results[:max_results]
    video_ids = [video.video_id for video in videos]
    return video_ids

# Funktion för att ladda ner video direkt
@st.cache_data
def download_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        filepath = f"{title}.mp4"
        ydl.download([url])
        return filepath

# Streamlit-gränssnitt
st.title("YouTube Video Sökare")

query = st.text_input("Skriv in sökord", "Streamlit tutorial")

if st.button("Sök"):
    video_ids = search_youtube(query)
    
    if video_ids:
        st.write(f"Hittade {len(video_ids)} videor")
        for video_id in video_ids:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            st.video(video_url)
            if st.button(f"Ladda ner {video_id}", key=f"download_{video_id}"):
                filepath = download_video(video_id)
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="Ladda ner video",
                        data=file,
                        file_name=os.path.basename(filepath),
                        mime="video/mp4"
                    )
                os.remove(filepath)
    else:
        st.write("Inga videor hittades")
