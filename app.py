import math
# from signal import signal
import altair as alt
import librosa
import librosa.display
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import altair as alt
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
# from sklearn.preprocessing import power_transform
import streamlit as st
import streamlit_vertical_slider as svs
# from scipy.fft import irfft, rfft, rfftfreq
from scipy.io import wavfile
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
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)

with open("style.css") as source_des:
    st.markdown(f"""<style>{source_des.read()}</style>""",
                unsafe_allow_html=True)

st.write(
    '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write(
    '<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
choose = st.radio("", ("Sin wave", "Music", "Vowels", "Biomedical Signal"))

# declare then in function function
if choose=='Sin wave'or choose=='Biomedical Signal':
    types="csv"
else:
    types="wav"

upload_col1, choose_col2 = st.columns([1, 3])
with upload_col1:
    upload_file = st.sidebar.file_uploader(" ",type=types)

 
n_spectro=st.sidebar.checkbox("spectrogram")
inver_btn=st.sidebar.button("Apply")



def sliders(no_col,writes=[]):
    sliders = []
    columns = st.columns(no_col,gap='small')
    for column  in columns:
        with column:
            slider = svs.vertical_slider(key=f"slider{columns.index(column)}",default_value=1,step=0.5,min_value=0,max_value=10,
                                        thumb_color="black", slider_color="black", track_color="grey")
            if slider == None:
                slider  = 1 
            sliders.append(slider) 
    
    for i in range(0, no_col):
        with columns[i]:
            slider_val = writes[i]
            st.write(f" { slider_val }")
    return sliders

time_col, inver_col = st.columns(2, gap='small')


def plot(t, magnitude):
    figure = px.line()
    figure.add_scatter(x=t, y=magnitude, mode='lines',
                       name='Uploaded Signal', line=dict(color='black'))
    figure.update_layout(width=500, height=300,
                         yaxis_title='Amplitude (mV)',
                         xaxis_title="Time (Sec)",
                         hovermode="x"
                         )
    st.plotly_chart(figure, use_container_width=True)
def plotting(df, ymin, ymax):
    fig_main=go.Figure()
    fig_main.add_trace(go.Line(x=df['x'],y=df['y'],name='orignal'))
    fig_main.update_layout(width=500,height=300,yaxis_range=[ymin, ymax],xaxis_title="Time(seconds)", yaxis_title="Amplitude")
    st.plotly_chart(fig_main, use_container_width=True)

def animation(t,signal):
    plot_spot=st.empty()
    df = pd.DataFrame({"x": t, "y": signal})
    ymax = max(df["y"])
    ymin = min(df["y"])
    for st.session_state['i'] in range(0,len(df)):
        df_tmp=df.iloc[st.session_state['i']:st.session_state['i']+3000,]
        with plot_spot:
            plotting(df_tmp, ymin, ymax)
        time.sleep(0.00000001) 

    


def plt_spectrogram(signal, fs):
    fig= plt.figure(figsize=(20,4))
    fig.tight_layout(pad=10.0)
    if choose=="Biomedical Signal":
        signal_d=signal[0:98]
    else:
        signal_d=signal
    plt.specgram(signal_d, Fs=fs,cmap="jet")
    plt.colorbar()
    st.pyplot(fig) 



def fourier_trans(magnitude=[], t=[], sr=0):
    n_samples = len(magnitude)
    if sr == 0:
        sample_period = t[1]-t[0]
        duration=n_samples*sample_period
    else:
        sample_period=1/sr
        duration = n_samples*sample_period
    full_mag=np.fft.rfft(magnitude)
    fft_frequencies = np.fft.rfftfreq(n_samples, sample_period)
    return fft_frequencies,full_mag,duration


def inverse_f(mag=[]):
    signal = np.fft.irfft(mag)
    return signal





def open_file(slider_v):
    if upload_file:
        if choose == "Sin wave" or choose == "Biomedical Signal":
            sr=0
            signal_upload = pd.read_csv(upload_file)
            t = signal_upload[signal_upload.columns[0]]
            signal_y = signal_upload[signal_upload.columns[1]]
        else:
            sr, signal = wavfile.read(upload_file)
            signal_y = signal[:, 0]
            t = np.arange(len(signal_y)) / float(sr)
        freq,full_mag,duration = fourier_trans(signal_y, t,sr)
        with time_col:
            plot(t, signal_y)
            if st.sidebar.checkbox("Dynamic"):
                animation(t,signal_y)
            if n_spectro:
                plt_spectrogram(signal_y, 2)        
            if choose == "Music" or choose == "Vowels"or choose =="Animals":
               st.audio(upload_file, format='audio/wav')
        
        if choose == "Sin wave":
            for i in range(0,10):
                full_mag[10*i:10*(i+1)]*=slider_v[i]

        elif choose == "Biomedical Signal":
            ranges=[0,60,90,250,300,600]
            for i,j in zip(range(len(slider_v)),range(0,len(ranges))):
                full_mag[ranges[j]:ranges[j+1]]*=slider_v[i]
        
      
        elif choose == "Vowels":
            ranges=[4433,8615,1800,17000]
            for i, j in zip(range(len(s_value)),range(0,len(ranges),2)):
                full_mag[int(duration*ranges[j]):int(duration*ranges[j+1])]*=s_value[i]
        if inver_btn:
            new_si = inverse_f(full_mag)
            with inver_col:
                plot(t, new_si)
                if n_spectro:
                    plt_spectrogram(new_si, 2)
                if choose == "Music" or choose == "Vowels"or choose =="Animals":
                        write('Edited_audio.wav', sr,  new_si .astype(np.int16))
                        st.audio('Edited_audio.wav', format='audio/wav')   


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if choose == "Sin wave":
    writes=[" 0 : 10 "," 10 : 20 "," 20 : 30"," 30 : 40"," 40 : 50 "," 50 : 60 "," 60 : 70 "," 70 : 80"," 80 : 90"," 90 : 100 "]
    s_value=sliders(no_col=10,writes=writes)

elif choose == "Biomedical Signal":
    writes=[" Bradycardia "," Normal_Range "," Atrial_Tachycardia "," Atrial_Flutter  "," Atrial_Fibrillation "]
    s_value = sliders(no_col=5,writes=writes)

elif choose == "Music":
    vowels=[" flute "," ACCORDION "," STEEL PAN ","sexaphone"]
    s_value = sliders(4,writes=vowels)
    
elif choose == "Vowels":
    writes=["S"," ch "]
    s_value = sliders(2,writes= writes)

open_file(s_value)
