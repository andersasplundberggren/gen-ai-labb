import streamlit as st
from pytube import Search, YouTube
import os

# Funktion som söker efter videor på YouTube utan API-nyckel
def search_youtube(query, max_results=3):
    search = Search(query)
    videos = search.results[:max_results]
    video_ids = [video.video_id for video in videos]
    return video_ids

# Funktion för att ladda ner video
@st.cache_data
def download_video(video_id):
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    video_stream = yt.streams.get_highest_resolution()
    download_path = f"video_{video_id}.mp4"
    video_stream.download(filename=download_path)
    return download_path

# Streamlit-gränssnitt
st.title("YouTube Video Sökare")

query = st.text_input("Skriv in sökord", "Streamlit tutorial")

if st.button("Sök"):
    video_ids = search_youtube(query)
    
    if video_ids:
        st.write(f"Hittade {len(video_ids)} videor")
        for video_id in video_ids:
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            if st.button(f"Ladda ner {video_id}", key=f"download_{video_id}"):
                filepath = download_video(video_id)
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="Ladda ner",
                        data=file,
                        file_name=filepath,
                        mime="video/mp4"
                    )
                os.remove(filepath)
    else:
        st.write("Inga videor hittades")
