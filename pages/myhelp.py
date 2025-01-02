import streamlit as st
from pytube import Search, YouTube
import tempfile

# Funktion som söker efter videor på YouTube utan API-nyckel
def search_youtube(query, max_results=3):
    search = Search(query)
    videos = search.results[:max_results]
    video_ids = [video.video_id for video in videos]
    return video_ids

# Funktion för att ladda ner video
def download_video(video_id):
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    video_stream = yt.streams.get_highest_resolution()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
        video_stream.download(output_path=tmpfile.name)
        return tmpfile.name

# Streamlit-gränssnitt
st.title("YouTube Video Sökare")

query = st.text_input("Skriv in sökord", "Streamlit tutorial")

if st.button("Sök"):
    video_ids = search_youtube(query)
    
    if video_ids:
        st.write(f"Hittade {len(video_ids)} videor")
        for video_id in video_ids:
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            if st.button(f"Ladda ner video {video_id}", key=video_id):
                filepath = download_video(video_id)
                with open(filepath, "rb") as file:
                    st.download_button(
                        label="Ladda ner",
                        data=file,
                        file_name=f"video_{video_id}.mp4",
                        mime="video/mp4"
                    )
    else:
        st.write("Inga videor hittades")
