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
# dow_btn, up_btn, pl_btn, ps_btn = st.columns([3, 3, 3, 3])
with buttons:
    download_btn = st.button('Download')
    signal_uploaded_file = st.file_uploader(
        "Upload file.csv or file.mp3 or file.wav", label_visibility="collapsed")
    #     time = signal_dataframe[0]
    #     amplitude = signal_dataframe[1]
    play_btn = st.button('Play')
    pause_btn = st.button("Pause")
with graph:
    fn.sig_plot()
with menu:
    st.image("signal_equalizer.png", width=100)

    choice = st.radio('Choose The Theme', options=[
                      'Frequency', 'Vowels', 'Musical Instrument', 'Biomedical Signal'])
    # st.write('this is a download btn.....')
st.write('this is the settings area contains setting sliders vertically.....')


if signal_uploaded_file:
    signal_dataframe = pd.read_csv(signal_uploaded_file)

# my_file = fn.popup_window(upload_btn)
# st.write(my_file)
