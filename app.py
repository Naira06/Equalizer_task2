import IPython.display as ipd
import librosa.display as lbd
import librosa as lbr
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import Functions as fn
import pandas as pd


# ___________________________ Styling _____________________________________
st.set_page_config(page_title="Equalizer",
                   page_icon="signal_equalizer.png", layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ___________________________________________________________________________


# _______________________________ Layout _______________________
buttons, graph, menu = st.columns([2, 14, 4])
with buttons:
    download_btn = st.button('Download')
    signal_uploaded_file = st.file_uploader(
        "Upload file.csv or file.mp3 or file.wav", label_visibility="collapsed")
    play_btn = st.button('Play')
    pause_btn = st.button("Pause")

with menu:
    st.image("signal_equalizer.png", width=100)

    choice = st.radio('Choose The Theme', options=[
                      'Frequency', 'Vowels', 'Musical Instrument', 'Biomedical Signal'])
with graph:
    if signal_uploaded_file:
        fn.wave_mp3_file_plot(signal_uploaded_file)
st.write('this is the settings area contains setting sliders vertically.....')
