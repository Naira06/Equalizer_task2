import math
from signal import signal
import altair as alt
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import power_transform
import streamlit as st
import streamlit_vertical_slider as svs
from scipy.fft import irfft, rfft, rfftfreq
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
            border: 1px solid transparent;
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)
# do/cument.getElemenTbyId("root").contentWindow.document.body.style.background="blue";
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
choose = st.radio("", ("Sin wave", "Music", "Vowels", "Biomedical Signal","change pitch"))
# declare then in function function



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
    if choose != "Sin wave":
        for i in range(0, no_col):
            with columns[i]:
                slider_val = writes[i]
                st.write(f" { slider_val }")
    return sliders

time_col, inver_col = st.columns(2, gap='small')


def plot(time, magnitude):
    figure = px.line()
    figure.add_scatter(x=time, y=magnitude, mode='lines',
                       name='Uploaded Signal', line=dict(color='black'))
    figure.update_layout(width=500, height=300,
                         yaxis_title='Amplitude (mV)',
                         xaxis_title="Time (Sec)",
                         hovermode="x"
                         )
                        #  paper_bgcolor='rgb(0,0,0,0)',
                        # plot_bgcolor='rgb(0,0,0,0)',
    st.plotly_chart(figure, use_container_width=True)


def plt_spectrogram(signal, fs):
    fig2 = plt.figure(figsize=(20, 4))
    plt.specgram(signal, Fs=fs,cmap="jet")
    plt.xlabel('time [sec]')
    plt.ylabel('Frequency [HZ]')
    fig2.savefig('spec')
    plt.colorbar()
    # ',transparent=True
    st.pyplot(fig2)



def fourier_trans(magnitude=[], time=[], sr=0):
    n_samples = len(magnitude)
    if sr == 0:
        sample_period = time[1]-time[0]
        duration=0
    else:
        sample_period=1/sr
        duration = n_samples*sample_period
        n_samples=round(sr*duration)
    full_mag=np.fft.rfft(magnitude)
    fft_magnitudes = np.abs(full_mag)
    fft_phase = np.angle(full_mag)
    fft_frequencies = np.fft.rfftfreq(n_samples, sample_period)
    return fft_magnitudes, fft_frequencies, fft_phase,full_mag,duration


def inverse_f(mag=[]):
    signal = np.fft.irfft(mag)
    return signal


def rect_form(mag=[], phase=[]):
    rect_array = []
    for i in range(len(mag)):
        rect_array.append(mag[i]*(math.cos(phase[i])+math.sin(phase[i])*1j))
        i += 1
    return rect_array

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
        inver_btn = st.sidebar.checkbox("Apply")
        signal_upload = pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]
        Mag, freq, f_mag,full_mag,duration = fourier_trans(signal_y, time)
        with time_col:
            plot(time, signal_y)
        if (st.sidebar.checkbox("Input spectro")):
            with time_col:
                plt_spectrogram(signal_y, 2)
        
        if choose == "Sin wave":
            min_frequency_value = int(len(freq)/10)
            columns = st.columns(10)
            for i in range(0, 10):
                with columns[i]:
                    frequency_val = (i)*min_frequency_value
                    st.write(f"  { frequency_val } HZ ")
            newarr = np.array_split(Mag, 10)
            for i in range(10):
                newarr[i] = newarr[i]*slider_v[i]
            arr = np.concatenate(newarr)
            with choose_col2:
                if inver_btn:
                    with inver_col:
                        new_rec = rect_form(arr, f_mag)
                        new_s = inverse_f(new_rec)
                        plot(time, new_s)
                        if (st.sidebar.checkbox("output spectro")):
                            plt_spectrogram(new_s, 2)
        elif choose == "Biomedical Signal":
            Bradycardia = slider_v[0]
            normal_range = slider_v[1]
            atrial_tachycardia = slider_v[2]
            Atrial_flutter = slider_v[3]
            Atrial_Fibrillation = slider_v[4]
            full_mag[0:60] *= Bradycardia
            full_mag[60:90] *= normal_range
            full_mag[90:250] *= atrial_tachycardia
            full_mag[250:300] *= Atrial_flutter
            full_mag[300:] *= Atrial_Fibrillation
            if inver_btn:
                new_si = inverse_f(full_mag)
                with inver_col:
                    plot(time, new_si)
                    if (st.sidebar.checkbox("output spectro")):
                        plt_spectrogram(new_si, 2)


def open_mp3(s_value):
    if upload_file:
        if choose=="Music":
            sr, yf = wavfile.read(upload_file)
            Mag, freq, f_mag,full_mag ,duration= fourier_trans(magnitude=yf, sr=sr)
            with time_col:
                yf1=np.ravel(yf)
                length = yf1.shape[0] / sr
                time = np.linspace(0., length,  yf1.shape[0])
                plot(time,yf1)
                if st.sidebar.checkbox("normal spectrogram"):
                   plt_spectrogram(yf1,sr)
                st.audio(upload_file, format='audio/wav')
            p_notes=getnotes()
            st.write(p_notes)
            m_signal=full_mag
            m_signal[int(duration*p_notes.get("G2")) :int(duration* p_notes.get("C8"))] *= sliders[0]    #drums
    
            m_signal[int(duration*0)  :int(duration* 450)] *= sliders[3]  #piano
         
            m_signal[int(duration*p_notes.get("C1")) :int(duration* p_notes.get("G7"))] *= sliders[2]   #guitar
                
        elif choose=="change pitch":
            signal_y,sr=librosa.load(upload_file)
            length = signal_y.shape[0] / sr
            time = np.linspace(0., length,  signal_y.shape[0])
            with time_col:
                plot(time,signal_y)
                if st.sidebar.checkbox("normal spectrogram"):
                   plt_spectrogram(signal_y,sr)
                st.audio(upload_file, format='audio/wav')
            pitch=st.sidebar.slider("Frequency of the added signal", min_value=-20,max_value=20)
            final_s=librosa.effects.pitch_shift(signal_y,sr=sr,n_steps=pitch)
            if st.sidebar.checkbox("Apply_ed"):
                with inver_col:
                    plot(time,  final_s)
                    if st.sidebar.checkbox("edit spectrogram"):
                     plt_spectrogram(final_s,sr)
                    norm=np.int16((final_s)*(32767/final_s.max()))
                    write('Edited_audio.wav' , round(sr ), norm)
                    st.audio('Edited_audio.wav', format='audio/wav')
        elif choose == "Vowels":
            sr, yf = wavfile.read(upload_file)
            yf1=np.ravel(yf)
            Mag, freq, f_mag,full_mag,duration = fourier_trans(magnitude=yf, sr=sr)
            with time_col:
                length =  yf1.shape[0] / sr
                time = np.linspace(0., length,  yf1.shape[0])
                plot(time,  yf1)
                if (st.sidebar.checkbox("Input spectro")):
                   with time_col:
                    plt_spectrogram(yf1, sr)
            y2 = full_mag[0:len(freq)]
            condition = ((freq > 500) & (freq < 1050))  # Letter A
            y2[condition] = y2[condition]*s_value[0]

            condition = ((freq > 1100) & (freq < 2000))  # Letter B
            y2[condition] = y2[condition]*s_value[1]

            condition = ((freq > 3000) & (freq < 4000))  # Letter D
            y2[condition] = y2[condition]*s_value[2]

            condition = ((freq > 5800) & (freq < 7000))  # Letter G
            y2[condition] = y2[condition]*s_value[3]
            y2 = inverse_f(y2)
            y2_id=np.ravel(y2)
        if (st.sidebar.checkbox("Apply")):
            if choose == "Music":
                with inver_col:
                    data = inverse_f(m_signal)
                    norm = np.int16(data*(32767/data.max()))
                    write('Edited_audio.wav', round(sr), norm)
                    st.sidebar.audio('Edited_audio.wav', format='audio/wav')
            else:
                with inver_col:
                    plot(time, y2_id)
                    if (st.sidebar.checkbox("output spectro")):
                     with inver_col:
                      plt_spectrogram( y2_id, sr)
                      write('Edited_audio.wav', sr, y2.astype(np.int16))
                     st.sidebar.audio('Edited_audio.wav', format='audio/wav')


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if choose == "Sin wave":
    s_value = sliders(no_col=10,writes=[])
    open_csv(s_value)
elif choose == "Biomedical Signal":
    #upload_file_plceholder.file_uploader("Browse", type=["csv"])
    # if upload_file:
    writes=[" Bradycardia "," Normal_Range "," Atrial_Tachycardia "," Atrial_Flutter  "," Atrial_Fibrillation "]
    s_value = sliders(no_col=5,writes=writes)
    open_csv(s_value)

elif choose == "Music" or choose == "Vowels"or choose =="change pitch":
    #upload_file_plceholder.file_uploader("Browse", type=["mp3"])
    # if upload_file:

    play, pause = st.columns([0.5, 5])
    #with play:
        #play_btn = st.button("▶️,⏭️,⏮️")
   # with pause:
        #pause_btn = st.button("⏸️")
    if choose == "Music":
        vowels=[" drums "," piano "," guitar "]
        s_value = sliders(3,writes=vowels)
        open_mp3(s_value)
    if choose == "Vowels":
        vowels=[" Letter A "," Letter B "," Letter D "," Letter G "]
        s_value = sliders(4,writes=vowels)
        open_mp3(s_value)
    if choose=="change pitch":
        s_value=0
        open_mp3(s_value)
