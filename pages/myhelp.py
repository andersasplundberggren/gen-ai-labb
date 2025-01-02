import streamlit as st
from pytube import Search

# Funktion som söker efter videor på YouTube utan API-nyckel
def search_youtube(query, max_results=3):
    search = Search(query)
    videos = search.results[:max_results]
    video_ids = [video.video_id for video in videos]
    return video_ids

# Streamlit-gränssnitt
st.title("YouTube Video Sökare")

query = st.text_input("Skriv in sökord", "Streamlit tutorial")

if st.button("Sök"):
    video_ids = search_youtube(query)
    
    if video_ids:
        st.write(f"Hittade {len(video_ids)} videor")
        for video_id in video_ids:
            st.video(f"https://www.youtube.com/watch?v={video_id}")
    else:
        st.write("Inga videor hittades")
