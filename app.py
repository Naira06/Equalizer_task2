import math
# from signal import signal
import altair as alt
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
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
choose = st.radio("", ("Sin wave", "Music", "Vowels", "Biomedical Signal","change pitch"))

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


def plot(time, magnitude):
    # df = pd.DataFrame({"x": time, "y": magnitude})
    
    figure = px.line()
    figure.add_scatter(x=time, y=magnitude, mode='lines',
                       name='Uploaded Signal', line=dict(color='black'))
    figure.update_layout(width=500, height=300,
                         yaxis_title='Amplitude (mV)',
                         xaxis_title="Time (Sec)",
                         hovermode="x"
                         )
    #                     #  paper_bgcolor='rgb(0,0,0,0)',
    #                     # plot_bgcolor='rgb(0,0,0,0)',
    st.plotly_chart(figure, use_container_width=True)


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



def fourier_trans(magnitude=[], time=[], sr=0):
    n_samples = len(magnitude)
    if sr == 0:
        sample_period = time[1]-time[0]
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

def getnotes():   
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 440 #Frequency of Note A4
    keys = np.array([x+str(y) for y in range(0,9) for x in octave])
    # Trim to standard 88 keys
    start = np.where(keys == 'A0')[0][0]
    end = np.where(keys == 'C8')[0][0]
    keys = keys[start:end+1]
    
    note_freqs = dict(zip(keys, [2**((n+1-49)/12)*base_freq for n in range(len(keys))]))
    note_freqs[''] = 0.0 # stop
    return note_freqs


def open_csv(slider_v):
    if upload_file:
        signal_upload = pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]
        freq,full_mag,duration = fourier_trans(signal_y, time)
        with time_col:
            plot(time, signal_y)
            if n_spectro:
                plt_spectrogram(signal_y, 2)
        
        if choose == "Sin wave":
            for i in range(0,10):
                full_mag[10*i:10*(i+1)]*=slider_v[i]

        elif choose == "Biomedical Signal":
            ranges=[0,60,90,250,300,600]
            for i,j in zip(range(len(slider_v)),range(0,len(ranges))):
                full_mag[ranges[j]:ranges[j+1]]*=slider_v[i]
        if inver_btn:
            new_si = inverse_f(full_mag)
            with inver_col:
                plot(time, new_si)
                if n_spectro:
                    plt_spectrogram(new_si, 2)


def open_mp3(s_value):
    if upload_file:
        if choose=="change pitch":
            signal_y,sr=librosa.load(upload_file)
            length = signal_y.shape[0] / sr
            time = np.linspace(0., length,  signal_y.shape[0])
            with time_col:
                plot(time,signal_y)
                if n_spectro:
                   plt_spectrogram(signal_y,sr)
                st.audio(upload_file, format='audio/wav')
            pitch=st.sidebar.slider("Frequency of the added signal", min_value=-20,max_value=20)
            final_s=librosa.effects.pitch_shift(signal_y,sr=sr,n_steps=pitch)
            if inver_btn:
                with inver_col:
                    plot(time,  final_s)
                    if n_spectro:
                     plt_spectrogram(final_s,sr)
                    norm=np.int16((final_s)*(32767/final_s.max()))
                    write('Edited_audio.wav' , round(sr ), norm)
                    st.audio('Edited_audio.wav', format='audio/wav')
        else:
            sr, signal = wavfile.read(upload_file)
            if choose=="Music":
                magnitude = signal[:, 0]
                time = np.arange(len(magnitude)) / float(sr)
                freq,full_mag ,duration= fourier_trans(magnitude=magnitude , sr=sr)
                with time_col:
                    plot(time,magnitude)
                    if n_spectro:
                        plt_spectrogram(magnitude,sr)
                    st.audio(upload_file, format='audio/wav')
                p_notes=getnotes()
                f_signal=full_mag
               
                # f_signal[int(duration*p_notes.get("G2")) :int(duration*p_notes.get("C8"))] *= sliders[0]    #drums
                f_signal[int(duration*900) :int(duration* 6000)] *= 1.15 *s_value[0] #flute
                f_signal[int(duration*500) :int(duration* 8000)] *= s_value[1]   #ACCORDION
                f_signal[int(duration*0) :int(duration* 2000)] *= s_value[2]   #STEEL PAN
                # f_signal[int(duration*26) :int(duration* 1300)] *= s_value[3]   #drums
                # f_signal[int(duration*70) :int(duration* 6300)] *= s_value[4]   #oud
                f_signal[int(duration*2000) :int(duration* 12000)] *= s_value[3]   #sexaphone
                if inver_btn:
                    with inver_col:
                        data = inverse_f(f_signal)
                        plot(time,data)
                        if n_spectro:
                            plt_spectrogram(data,sr) 
                        norm = np.int16(data*(32767/data.max()))
                        write('Edited_audio.wav', round(sr), norm)
                        st.audio('Edited_audio.wav', format='audio/wav')
            elif choose == "Vowels":
                signal_y=np.ravel(signal)
                freq,full_mag,duration = fourier_trans(magnitude=signal, sr=sr)
                with time_col:
                    length =  signal_y.shape[0] / sr
                    time = np.linspace(0., length,  signal_y.shape[0])
                    plot(time, signal_y)
                    if n_spectro:
                        with time_col:
                            plt_spectrogram(signal_y, sr)
                        st.audio(upload_file, format='audio/wav')
                v_signal = full_mag[0:len(freq)]
                condition = ((freq > 500) & (freq < 1050))  # Letter A
                v_signal[condition] = v_signal[condition]*s_value[0]

                condition = ((freq > 1100) & (freq < 2000))  # Letter B
                v_signal[condition] = v_signal[condition]*s_value[1]

                condition = ((freq > 3000) & (freq < 4000))  # Letter D
                v_signal[condition] = v_signal[condition]*s_value[2]

                condition = ((freq > 5800) & (freq < 7000))  # Letter G
                v_signal[condition] = v_signal[condition]*s_value[3]
                v_signal = inverse_f(v_signal)
                f_signal=np.ravel(v_signal)
                if inver_btn:
                    with inver_col:
                        plot(time, f_signal)
                        st.sidebar.audio('Edited_audio.wav', format='audio/wav')
                        if n_spectro:
                            plt_spectrogram( f_signal, sr)
                            write('Edited_audio.wav', sr, v_signal.astype(np.int16))
                            st.audio('Edited_audio.wav', format='audio/wav')    


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if choose == "Sin wave" or choose == "Biomedical Signal":
    if choose == "Sin wave":
        writes=[" 0 : 10 "," 10 : 20 "," 20 : 30"," 30 : 40"," 40 : 50 "," 50 : 60 "," 60 : 70 "," 70 : 80"," 80 : 90"," 90 : 100 "]
        s_value=sliders(no_col=10,writes=writes)
   
    elif choose == "Biomedical Signal":
        writes=[" Bradycardia "," Normal_Range "," Atrial_Tachycardia "," Atrial_Flutter  "," Atrial_Fibrillation "]
        s_value = sliders(no_col=5,writes=writes)
    open_csv(s_value)

elif choose == "Music" or choose == "Vowels"or choose =="change pitch":
    if choose == "Music":
        vowels=[" flute "," ACCORDION "," STEEL PAN ","sexaphone"]
        s_value = sliders(4,writes=vowels)
        
    elif choose == "Vowels":
        vowels=[" Letter A "," Letter B "," Letter D "," Letter G "]
        s_value = sliders(4,writes=vowels)
        
    elif choose=="change pitch":
        s_value=0
    open_mp3(s_value)
