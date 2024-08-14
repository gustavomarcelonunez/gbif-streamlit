import streamlit as st

@st.dialog('BotGBIF Demo')
def show_video():
    video_file = open("BotGBIF-DEMO.mp4", "rb")
    video_bytes = video_file.read()
    st.video(video_bytes)