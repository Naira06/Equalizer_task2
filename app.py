import streamlit as st
import numpy as np
import Functions as fn


t = np.linspace(0, 1, 1000)
v = 15*np.sin(20*np.pi*t)


graph, menu = st.columns([8, 1])
settings, choices = st.columns([8, 1])
with graph:
    fn.sig_plot(t, v, 'Time', "Voltage")
with menu:
    # st.write('this is a download btn.....')
    download_btn = st.button('Download')
    upload_btn = st.button('Upload')
    play_pause_btn = st.button('Play/Pause')
with settings:
    st.write('this is the settings area contains setting sliders vertically.....')
with choices:
    choice = st.radio('Choose The Theme', options=[
                      'Frequency', 'Vowels', 'Musical Instrument', 'Biomedical Signal'])

my_file = fn.popup_window(upload_btn)
st.write(my_file)
