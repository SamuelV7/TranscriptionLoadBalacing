import streamlit as st
from main import whisper

st.write("Hello World")

# let user upload file
uploaded_file = st.file_uploader("Choose a file")