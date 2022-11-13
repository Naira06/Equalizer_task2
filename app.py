import streamlit as st
import pandas as pd
import numpy as np
import math
import altair as alt
import librosa
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit_vertical_slider as svs
from scipy.io.wavfile import write

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
            border: 1px solid transparent;

        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)
with open("style.css") as source_des:
    st.markdown(f"""<style>{source_des.read()}</style>""",
                unsafe_allow_html=True)
upload_col1, choose_col2 = st.columns([1, 3])
with upload_col1:
    # upload_file_plceholder=st.empty()
    # upload_file=upload_file_plceholder.file_uploader("Browse", type=["csv"], key="uploader")
    upload_file = st.sidebar.file_uploader(" ")

st.write(
    '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write(
    '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
choose = st.radio("", ("Sin wave", "Music", "Vowels", "Biomedical Signal"))
# declare then in function function



def sliders(num=9):
    groups = [(0, 1),
              (1, 1),
              (2, 1),
              (3, 1),
              (4, 1),
              (5, 1),
              (6, 1),
              (7, 1),
              (8, 1),
              (9, 1)
              ]

    sliders = {}
    columns = st.columns(len(groups), gap='small')

    for idx, i in enumerate(groups):
        min_value = 0
        max_value = 5
        key = idx
        with columns[idx]:
            sliders[key] = svs.vertical_slider(
                key=key, default_value=1, step=1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key] = i[1]
    # if choose != "Sin Wave":
    #     for i in range(0, num):
    #         with columns[i]:
    #                 s_value = writes=[i]
    #                 st.write(f" { s_value }")
        if idx == num:
            return sliders


time_col,inver_col = st.columns(2, gap='small')


def plot(time, magnitude):
    figure = px.line()
    figure.add_scatter(x=time, y=magnitude, mode='lines',
                       name='Uploaded Signal', line=dict(color='blue'))
    figure.update_layout(width=500, height=300,
                         template='simple_white',
                         yaxis_title='Amplitude (mV)',
                         xaxis_title="Time (Sec)",
                         hovermode="x")
    st.plotly_chart(figure, use_container_width=True)
    


def plt_spectrogram(signal, fs):
    fig2 = plt.figure(figsize=(20, 4))
    plt.specgram(signal, Fs=fs)
    plt.colorbar()
    st.pyplot(fig2)

def fourier_trans(magnitude=[], time=[], sr=0):
    if sr == 0:
        sample_period = time[1]-time[0]
    else:
        sample_period = sr
    n_samples = len(magnitude)
    fft_magnitudes = np.abs(np.fft.rfft(magnitude))
    fft_phase = np.angle(np.fft.rfft(magnitude))
    fft_frequencies = np.fft.rfftfreq(n_samples, sample_period)
    return fft_magnitudes, fft_frequencies, fft_phase


def inverse_f(mag=[], time=[]):
    signal = np.fft.irfft(mag)
    return signal


def rect_form(mag=[], phase=[]):
    rect_array = []
    for i in range(len(mag)):
        rect_array.append(mag[i]*(math.cos(phase[i])+math.sin(phase[i])*1j))
        i += 1
    return rect_array


def open_csv(slider_v):
    if upload_file:
        inver_btn = st.sidebar.checkbox("Apply")
        signal_upload = pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]

        with time_col:
            plot(time, signal_y)
        if (st.sidebar.checkbox("Input spectro")):
            with time_col:
                plt_spectrogram(signal_y, 2)
        Mag, freq, f_mag = fourier_trans(signal_y, time)
        if choose == "Sin wave":
        #     min_frequency_value = int(len(freq)/10)
        #     columns = st.columns(10)
        #     for i in range(0, 10):
        #         with columns[i]:
        #             frequency_val = (i)*min_frequency_value
        #             st.write(f"  { frequency_val } HZ ")
            newarr = np.array_split(Mag, 10)
            for i in range(10):
                newarr[i] = newarr[i]*slider_v[i]
            arr = np.concatenate(newarr)
            with choose_col2:
                if inver_btn:
                    with inver_col:
                        new_rec = rect_form(arr, f_mag)
                        new_s = inverse_f(new_rec, time)
                        plot(time, new_s)
                        if (st.sidebar.checkbox("output spectro")):
                            plt_spectrogram(new_s,2)
        elif choose == "Biomedical Signal":
            Bradycardia = slider_v[0]
            normal_range = slider_v[1]
            atrial_tachycardia = slider_v[2]
            Atrial_flutter = slider_v[3]
            Atrial_Fibrillation = slider_v[4]
            Mag[0:60] *= Bradycardia
            Mag[60:90] *= normal_range
            Mag[90:250] *= atrial_tachycardia
            Mag[250:300] *= Atrial_flutter
            Mag[300:] *= Atrial_Fibrillation
            if inver_btn:
                new_re = rect_form(Mag, f_mag)
                new_si = inverse_f(new_re, time)
                with inver_col:
                    plot(time, new_si)
                    if (st.sidebar.checkbox("output spectro")):
                        plt_spectrogram(new_si,2)


def open_mp3(s_value):
    if upload_file:
        with choose_col2:
            st.audio(upload_file, format='audio/wav')
        yf, sr = librosa.load(upload_file)
        length = yf.shape[0] / sr
        time = np.linspace(0., length, yf.shape[0])
        with time_col:
            plot(time, yf)
            if (st.sidebar.checkbox("spectro")):
                plt_spectrogram(yf.sr)
        Mag, freq, f_mag = fourier_trans(magnitude=yf, sr=sr)
        if (st.sidebar.button("Apply")):
            new_rec = rect_form(Mag, f_mag)
            data = inverse_f(new_rec, time)
            norm = np.int16(data*(32767/data.max()))
            write('Edited_audio.wav', round(sr), norm)
            st.sidebar.audio('Edited_audio.wav', format='audio/wav')
            # write("Edited_audio.wav",sr,data.astype(np.int16))
            #st.sidebar.audio('Edited_audio.wav' , format= 'audio/wav')


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if choose == "Sin wave":
    s_value = sliders(9)
    open_csv(s_value)
elif choose == "Biomedical Signal":
    #upload_file_plceholder.file_uploader("Browse", type=["csv"])
    # if upload_file:
    #writes=[" Bradycardia "," Normal_Range "," Atrial_Tachycardia "," Atrial_Flutter  "," Atrial_Fibrillation "]
    s_value = sliders(4)
    open_csv(s_value)

elif choose == "Music" or choose == "Vowels":
    #upload_file_plceholder.file_uploader("Browse", type=["mp3"])
    # if upload_file:

    play, pause = st.columns([0.5, 5])
    with play:
        play_btn = st.button("▶️,⏭️,⏮️")
    with pause:
        pause_btn = st.button("⏸️")
    if choose == "Music":
        s_value = sliders(3)
        open_mp3(s_value)
    if choose == "Vowels":
        s_value = sliders(9)
        open_mp3(s_value)






