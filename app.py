import streamlit as st
import pandas as pd
import numpy as np
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
with st.container():
    upload_col1, choose_col2 = st.columns(2)
    with upload_col1:
        # upload_file_plceholder=st.empty()
        # upload_file=upload_file_plceholder.file_uploader("Browse", type=["csv"], key="uploader")   
        upload_file=st.file_uploader(" ") 
with  choose_col2:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose=st.radio("",("Sin wave","Music","Vowels","Biomedical Signal"))
  #declare then in function function


def sliders(num,min,max):
    groups = [(0,num) ,
            (1,num),
            (2,num),
            (3,num),
            (4,num),
            (5,num),
            (6,num),
            (7,num),
            (8,num),
            (9,num)
    ]

    sliders = {}
    columns = st.columns(len(groups),gap='small')

    for idx, i in enumerate(groups):
        min_value =min
        max_value = max
        key = idx
        with columns[idx]:
            sliders[key] = svs.vertical_slider(key=key, default_value=num,step=1, min_value=min_value, max_value=max_value)
            if sliders[key] == None:
                sliders[key]  = num
    return sliders

time_col,freq_col=st.columns(2,gap='small')  

def plot(time,magnitude):
    with time_col:
        figure =px.line()
        figure.add_scatter(x=time, y=magnitude,mode='lines',name='Uploaded Signal',line=dict(color='blue'))
        figure.update_layout(width=5000, height=500,
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
        figure_1.update_layout(width=5000, height=500,
                            template='simple_white',
                            yaxis_title='FFT Amplitude |X(freq)|)',
                            xaxis_title="Frequency (HZ)",
                            hovermode="x")
        

def fourier_trans(magnitude=[],time=[]):
    sample_period = time[1]-time[0]
    n_samples = len(time)//2
    fft_magnitudes=np.abs(np.fft.fft(magnitude))
    fft_frequencies = np.fft.fftfreq(n_samples, sample_period)
    plot_freq(fft_frequencies,fft_magnitudes)
    return fft_magnitudes,fft_frequencies;
# def inverse_f(mag=[],freq=[]):
#     result = 1j*freq; 
#     result += mag
#     st.write(result)
#     signal=np.fft.irfft(result)
#     st.write(signal)
#     fig2.px.line(x=)
    

def open_csv(slider_v):
    if upload_file:
        signal_upload=pd.read_csv(upload_file)
        time = signal_upload[signal_upload.columns[0]]
        signal_y = signal_upload[signal_upload.columns[1]]
        plot(time,signal_y)
        Mag,freq=fourier_trans( signal_y , time)
        newarr = np.array_split(Mag,10 )
        for i in range(10):
            newarr[i]=newarr[i]*slider_v[i]
        arr = np.concatenate((newarr))  
        with freq_col:
            global figure_1
            figure_1.add_trace(go.Line(x=freq,y=arr,name='Sliders_Frequency',line=dict(color='#FF0000')))
            st.plotly_chart(figure_1, use_container_width=True)
        
def open_mp3():
    if upload_file:
        Audio=st.audio(upload_file, format='audio/mp3')
        return Audio

if choose =="Sin wave" or choose =="Biomedical Signal":
        #upload_file_plceholder.file_uploader("Browse", type=["csv"])    
        #if upload_file:
        s_value=sliders(1,0,5)
        open_csv(s_value)
           
           
           
elif choose =="Music" or choose =="Vowels":
        #upload_file_plceholder.file_uploader("Browse", type=["mp3"])    
        #if upload_file:
        open_mp3()
        play,pause= st.columns([0.5,5])
        with play:
            play_btn=st.button("Play")
        with pause:
            pause_btn=st.button("pause")


    