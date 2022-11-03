import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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
