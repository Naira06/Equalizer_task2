import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import librosa as lbr
import librosa.display as lbd
import IPython.display as ipd

from itertools import cycle

sns.set_theme(style="dark", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

# ipd.Audio("Believer.mp3").autoplay
# read mp3 file
amp, sampla_rate = lbr.load("Believer.mp3")

# print(f"Shape of amp: {amp.shape}")
# print(f"Length of amp: {len(amp)}")
# print(f"Sample Rate: {sampla_rate}")

# pd.Series(amp).plot(figsize=(10, 5))
# plt.show()

freq_domain = lbr.stft(amp)
s_dB = lbr.amplitude_to_db(np.abs(freq_domain), ref=np.max)
# print(s_dB.shape)

fig, ax = plt.subplots(figsize=(10, 5))
img = lbd.specshow(s_dB, x_axis='time', y_axis='log', ax=ax)
fig.colorbar(img, ax=ax, format=f'%0.2f')
plt.show()

# print(freq_domain)
