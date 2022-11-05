import streamlit as st
import pandas as pd
import numpy as np
from math import ceil, floor
import plotly.express as px
import streamlit_vertical_slider as svs

st.set_page_config(page_title="Equalizer",
                   page_icon=":headphones:", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
button_style = """
        <style>
        .stButton > button {
            width: 90px;
            height: 35px;
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)


def plot(time, magnitude):
    figure = px.line()
    figure.add_scatter(x=time, y=magnitude, mode='lines',
                       name='Uploaded Signal', line=dict(color='blue'))
    figure.update_layout(width=5000, height=500,
                         template='simple_white',
                         yaxis_title='Amplitude (V)',
                         xaxis_title="Time (Sec)",
                         hovermode="x")
    st.plotly_chart(figure, use_container_width=True)


def plot_freq(frequencies, magnitudes):
    figure = px.line()
    figure.add_scatter(x=frequencies, y=magnitudes, mode='lines',
                       name='Uploaded Signal', line=dict(color='blue'))
    figure.update_layout(width=5000, height=500,
                         template='simple_white',
                         yaxis_title='FFT Amplitude |X(freq)|)',
                         xaxis_title='Frequency (Hz)',
                         hovermode="x")
    st.plotly_chart(figure, use_container_width=True)


def fourier_trans(magnitude=[], time=[]):
    sample_period = time[1]-time[0]
    n_samples = len(time)
    fft_magnitudes = np.abs(np.fft.fft(magnitude))
    fft_frequencies = np.fft.fftfreq(n_samples, sample_period)
    # for idx, i in enumerate(groups):

    plot_freq(fft_frequencies, fft_magnitudes)


def open_csv():
    if upload_file:
        signal_upload = pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]
        with col1:
            plot(time, signal_y)
        fourier_trans(signal_y, time)


def open_mp3():
    if upload_file:
        Audio = st.audio(upload_file, format='audio/mp3')
        return Audio


with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # upload_file_plceholder=st.empty()
        # upload_file=upload_file_plceholder.file_uploader("Browse", type=["csv"], key="uploader")
        upload_file = st.file_uploader("Browse")

  # declare then in function function


with col2:
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write(
        '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose = st.radio("", ("Sin wave", "Music", "Vowels", "Biomedical Signal"))
    if choose == "Sin wave" or choose == "Biomedical Signal":
        #upload_file_plceholder.file_uploader("Browse", type=["csv"])
        # if upload_file:
        open_csv()

    elif choose == "Music" or choose == "Vowels":
        #upload_file_plceholder.file_uploader("Browse", type=["mp3"])
        # if upload_file:
        open_mp3()


groups = [('slider1', 50),
          ('slider2', 150),
          ('slider3', 250),
          ('slider4', 350),
          ('slider5', 450),
          ('slider6', 550),
          ('slider7', 650),
          ('slider8', 750),
          ('slider9', 850),
          ('slider10', 950),
          ]
boundary = int(50)
adjusted_data = []
sliders = {}
columns = st.columns(len(groups), gap='small')

for idx, i in enumerate(groups):
    if i[0] != 'slider1':
        min_value = i[1] + 1 - boundary
    else:
        min_value = i[1] - boundary
    max_value = i[1] + boundary
    key = f'member{str(idx)}'
    with columns[idx]:
        sliders[f'slider_group_{key}'] = svs.vertical_slider(key=key, default_value=i[1],
                                                             step=1, min_value=min_value, max_value=max_value)
        if sliders[f'slider_group_{key}'] == None:
            sliders[f'slider_group_{key}'] = i[1]
        adjusted_data.append((i[0], sliders[f'slider_group_{key}']))
# with st.container():
play, pause = st.columns([0.5, 5])
with play:
    play_btn = st.button("Play")
with pause:
    pause_btn = st.button("pause")
