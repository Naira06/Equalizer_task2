import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import Functions as fn
import plotly_express as px
import plotly.graph_objects as go


t = np.linspace(0, 1, 1000)
v = 15*np.sin(20*np.pi*t)


graph, menu = st.columns([8, 1])
settings, choices = st.columns([8, 1])
with graph:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t,
        y=v,
    ))

    fig.update_layout(
        autosize=True,
        width=500,
        height=150,
        margin=dict(
            l=0,
            r=0,
            b=10,
            t=10,
            pad=0
        ),
        paper_bgcolor="#fff",
    )
    st.plotly_chart(fig, True)
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
