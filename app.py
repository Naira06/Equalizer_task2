import streamlit as st
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
