import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import streamlit_modal as modal
import streamlit.components.v1 as components

# ____________________________ convert two arrays to a dataframe ______________


def convert_to_dataframe(par1, par2, par1_name, par2_name):
    signal = []
    for i in range(len(par1)):
        signal.append([par1[i], par2[i]])
    return pd.DataFrame(signal, columns=[f'{par1_name}', f'{par2_name}'])

# ____________________________ plot two arrays in streamlit ______________


def plot_two_arrays(x_axis, y_axis, x_axis_label, y_axis_label):
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.set_xlabel(f'{x_axis_label}')
    ax.set_ylabel(f'{y_axis_label}')
    st.plotly_chart(fig, True)


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
