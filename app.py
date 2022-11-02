import streamlit as st
import pandas as pd
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
    col1, col2 = st.columns(2)
    with col1:
        upload_file_plceholder=st.empty()
        upload_file=upload_file_plceholder.file_uploader("Browse", type=["csv"], key="uploader")    
    
  #declare then in function function
def open_csv():
    signal_upload=pd.read_csv(upload_file)
    return signal_upload
def open_mp3():
    if upload_file.type!="mp3":
        st.error(" wrong Extension, Requierd *.mp3* ")
    else:
      Audio=st.audio(upload_file, format='audio/mp3')
    return Audio
with  col2:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose=st.radio("",("Sine wave","Music","Vowels","Biomedical Signal"))
    if choose =="Sine wave" or choose =="Biomedical Signal":
        upload_file_plceholder.file_uploader("Browse", type=["csv"])    
        if upload_file:
          open_csv()
    elif choose =="Music" or choose =="Vowels":
        upload_file_plceholder.file_uploader("Browse", type=["mp3"])    
        if upload_file:
          open_mp3()



groups = [('slider1',50),
            ('slider2',150),
            ('slider3',250),
            ('slider4',350),
            ('slider5',450),
            ('slider6',550),
            ('slider7',650),
            ('slider8',750),
            ('slider9',850),
            ('slider10',950),
]
boundary = int(50)
adjusted_data = []
sliders = {}
columns = st.columns(len(groups),gap='small')

for idx, i in enumerate(groups):
    min_value = i[1] - boundary
    max_value = i[1] + boundary
    key = f'member{str(idx)}'
    with columns[idx]:
        sliders[f'slider_group_{key}'] = svs.vertical_slider(key=key, default_value=i[1],
         step=1, min_value=min_value, max_value=max_value)
        if sliders[f'slider_group_{key}'] == None:
            sliders[f'slider_group_{key}']  = i[1]
        adjusted_data.append((i[0],sliders[f'slider_group_{key}'] ))
#with st.container():
play,pause= st.columns([0.5,5])
with play:
    play_btn=st.button("Play")
with pause:
    pause_btn=st.button("pause")

    