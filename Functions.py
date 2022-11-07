import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import streamlit_modal as modal
import streamlit.components.v1 as components
import plotly_express as px
import plotly.graph_objects as go
import numpy as np
import librosa as lbr


# ____________________________ convert two arrays to a dataframe ______________


def convert_to_dataframe(par1, par2, par1_name, par2_name):
    signal = []
    for i in range(len(par1)):
        signal.append([par1[i], par2[i]])
    return pd.DataFrame(signal, columns=[f'{par1_name}', f'{par2_name}'])


# ____________________________ plot two arrays in streamlit ______________
def sig_plot(x_axis=np.linspace(0, 1, 1000), y_axis=15*np.sin(0*np.pi*(np.linspace(0, 1, 1000))), x_axis_label="Time", y_axis_label="Voltage"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_axis,
        y=y_axis,
    ))
    fig.update_layout(
        autosize=True,
        width=500,
        height=350,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="rgba(204,82,159,0.01)",
        xaxis_title=f"{x_axis_label}",
        yaxis_title=f"{y_axis_label}",
        font=dict(color="white", size=12),
        template="plotly_dark",
    )
    st.plotly_chart(fig, True)


# ____________________________ Spectrogram _____________________
def spectrogram_plot(amp):
    amp_forier = lbr.stft(amp)
    S_db = lbr.amplitude_to_db(np.abs(amp_forier), ref=np.max)
    fig, ax = plt.subplots(figsize=(10, 5))
    img = lbr.display.specshow(S_db,
                               x_axis='time',
                               y_axis='log',
                               ax=ax)
    ax.set_title('Spectogram Example', fontsize=20)
    fig.colorbar(img, ax=ax, format=f'%0.2f')
    st.pyplot(fig)

# ______________________________________ Plotting mp3 and wav file ______________


def wave_mp3_file_plot(file_uploaded):
    if file_uploaded.name.split(".")[1] == 'mp3' or file_uploaded.name.split(".")[1] == 'wav':
        amp, sampla_rate = lbr.load(file_uploaded.name)
        t = []
        for i in range(len(amp)):
            t.append(i)
        # st.write(len(t))
        # st.write(len(amp))
        sig_plot(t, amp)
        st.audio(file_uploaded.name)
        # spectrogram_plot(amp)
        # st.write(len(amp))
    else:
        return


# _________________________________ Download csv file _____________________________
def download_csv_file(par1, par2, file_name, x_axis_label, y_axis_label):

    signal_analysis_table = convert_to_dataframe(
        par1, par2, x_axis_label, y_axis_label)
    signal_csv = signal_analysis_table.to_csv()
    st.download_button('Download CSV file', signal_csv,
                       f'signal_{file_name}.csv')


# ________________________________ Popup window __________________________________________
def popup_window(open_modal):
    uplaoded_file = ""
    if open_modal:
        modal.open()
    if modal.is_open():
        with modal.container():
            uplaoded_file = st.file_uploader(
                'Upload CSV or Audio_file.wave/.mp3')
            sub_btn = st.button('Submit')
            if sub_btn:
                if uplaoded_file:
                    return uplaoded_file


# _______________________________ Convert csv to dataframe ___________
def csv_to_arr(signal_uploaded_file):
    signal_dataframe = pd.read_csv(signal_uploaded_file)
    time = signal_dataframe['Time']
    amplitude = signal_dataframe["Amplitude"]
    return time, amplitude
