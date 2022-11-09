import streamlit as st
import pandas as pd
import numpy as np
import math
import librosa
import plotly.graph_objects as go
import plotly.express as px
import  streamlit_vertical_slider  as svs

st.set_page_config(page_title="Equalizer", page_icon=":headphones:",layout="wide")


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
    st.markdown(f"""<style>{source_des.read()}</style>""", unsafe_allow_html=True)
with st.container():
    upload_col1, choose_col2 = st.columns([1,3])
    with upload_col1:
        # upload_file_plceholder=st.empty()
        # upload_file=upload_file_plceholder.file_uploader("Browse", type=["csv"], key="uploader")   
        upload_file=st.file_uploader(" ") 
with  choose_col2:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose=st.radio("",("Sin wave","Music","Vowels","Biomedical Signal"))
  #declare then in function function


def sliders(num=10):
    groups = [(0,1) ,
            (1,1),
            (2,1),
            (3,1),
            (4,1),
            (5,1),
            (6,1),
            (7,1),
            (8,1),
            (9,1)
    ]

    sliders = {}
    columns = st.columns(len(groups),gap='small')

    for idx, i in enumerate(groups):
        min_value =0
        max_value = 5
        key = idx
        with columns[idx]:
            sliders[key] = svs.vertical_slider(key=key, default_value=1,step=1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key]  = i[1]
        if idx==num:
            return sliders

time_col,freq_col,inver_col=st.columns(3,gap='small')  

def plot(time,magnitude):
    with time_col:
        figure =px.line()
        figure.add_scatter(x=time, y=magnitude,mode='lines',name='Uploaded Signal',line=dict(color='blue'))
        figure.update_layout(width=500, height=400,
                            template='simple_white',
                            yaxis_title='Amplitude (V)',
                            xaxis_title="Time (Sec)",
                            hovermode="x")
        st.plotly_chart(figure, use_container_width=True)


def plot_freq(frequencies,magnitudes):
    with freq_col:
        global figure_1
        figure_1 =px.line()
        figure_1.add_scatter(x=frequencies, y=magnitudes,mode='lines',name='Uploaded Signal',line=dict(color='blue'))
        figure_1.update_layout(width=500, height=400,
                            template='simple_white',
                            yaxis_title='FFT Amplitude |X(freq)|)',
                            xaxis_title="Frequency (HZ)",
                            hovermode="x")
        #st.plotly_chart(figure_1, use_container_width=True)

def fourier_trans(magnitude=[],time=[],sr=0):
    if sr==0:
        sample_period = time[1]-time[0]
    else:
        sample_period=sr
    n_samples = len(magnitude)
    fft_magnitudes=np.abs(np.fft.rfft(magnitude))
    fft_phase=np.angle(np.fft.rfft(magnitude))
    fft_frequencies = np.fft.rfftfreq(n_samples, sample_period)
    plot_freq(fft_frequencies,fft_magnitudes)
    return fft_magnitudes,fft_frequencies,fft_phase
def inverse_f(mag=[],time=[]):
    signal=np.fft.irfft(mag)
    with inver_col:
        fig3=px.line(x=time,y=signal)
        fig3.update_layout(width=500, height=400,
                            template='simple_white',
                            yaxis_title='Amplitude (V)',
                            xaxis_title="Time (Sec)",
                            hovermode="x")
        st.plotly_chart(fig3, use_container_width=True)

def rect_form(mag=[],phase=[]):
    rect_array=[]
    for i in range(len(mag)):
        rect_array.append(mag[i]*(math.cos(phase[i])+math.sin(phase[i])*1j))
        i += 1
    return rect_array

  
def open_csv(slider_v):
    if upload_file:
        signal_upload=pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]
        plot(time,signal_y)
        Mag,freq,f_mag=fourier_trans( signal_y , time)
        newarr = np.array_split(Mag,10)
        #newarr=[f_mag]
        for i in range(10):
            newarr[i]=newarr[i]*slider_v[i]
        arr = np.concatenate((newarr))  
        with choose_col2:
            if st.checkbox("inverse"):
                new_rec=rect_form(arr,f_mag)
                inverse_f(new_rec,time)
        with freq_col:
            global figure_1
            figure_1.add_trace(go.Line(x=freq,y=arr,name='Sliders_Frequency',line=dict(color='#FF0000')))
            st.plotly_chart(figure_1, use_container_width=True)
        
def open_mp3(slider_v):
    if upload_file:
        with choose_col2:
            st.audio(upload_file, format='audio/wav')
        yf,sr=librosa.load(upload_file)
        length = yf.shape[0] / sr
        time = np.linspace(0., length, yf.shape[0])    
        plot(time,yf)
        Mag,freq,f_mag=fourier_trans(magnitude=yf,sr=sr)
        with freq_col:
            global figure_1
            figure_1.add_trace(go.Line(x=freq,y=Mag,name='Sliders_Frequency',line=dict(color='#FF0000')))
            st.plotly_chart(figure_1, use_container_width=True)
        if (st.sidebar.button("Apply")):
            new_rec=rect_form(Mag,f_mag)
            inverse_f(new_rec,time)
           
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if choose =="Sin wave" :
    s_value=sliders(9)
    open_csv(s_value)
elif choose =="Biomedical Signal":
        #upload_file_plceholder.file_uploader("Browse", type=["csv"])    
        #if upload_file:
        s_value=sliders(3)
        open_csv(s_value)
                     
elif choose =="Music" or choose =="Vowels":
        #upload_file_plceholder.file_uploader("Browse", type=["mp3"])    
        #if upload_file:
        
        play,pause= st.columns([0.5,5])
        with play:
            play_btn=st.button("▶️,⏭️,⏮️")
        with pause:
            pause_btn=st.button("⏸️")
        if choose =="Music":
         s_value=sliders(3)
         open_mp3(s_value) 
        if choose =="Vowels":
            s_value=sliders(9)
            open_mp3(s_value)



