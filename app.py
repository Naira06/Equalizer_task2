import streamlit as st
import numpy as np
import Functions as fn
import pandas as pd


t = np.linspace(0, 1, 1000)
v = 15*np.sin(20*np.pi*t)


graph, menu = st.columns([11, 4])
dow_btn, up_btn, pl_btn, ps_btn = st.columns([3, 3, 3, 3])
with graph:
    fn.sig_plot(t, v, 'Time', "Voltage")

with dow_btn:
    download_btn = st.button('Download')
with up_btn:
    upload_btn = st.button('Upload')
with pl_btn:
    play_btn = st.button('Play')
with ps_btn:
    pause_btn = st.button("Pause")
with menu:
    choice = st.radio('Choose The Theme', options=[
                      'Frequency', 'Vowels', 'Musical Instrument', 'Biomedical Signal'])
    # st.write('this is a download btn.....')
signal_dataframe = ''
if upload_btn:
    signal_uploaded_file = st.file_uploader(
        "Upload file.csv or file.mp3 or file.wav")
    if signal_uploaded_file:
        signal_dataframe = pd.read_csv(signal_uploaded_file)
        time = signal_dataframe[0]
        amplitude = signal_dataframe[1]
st.write(signal_dataframe)
st.write('this is the settings area contains setting sliders vertically.....')


# my_file = fn.popup_window(upload_btn)
# st.write(my_file)
