# %%
from cProfile import label
import numpy as np
import os
import pandas as pd
import cv2
import skimage.io 
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
from glob import glob

import utility

start_wl = 304
stop_wl = 453

df_sds5_C = pd.read_csv('sds5_C_reflectance.csv')
df_sds5_H = pd.read_csv('sds5_H_reflectance.csv')
df_sds5_I = pd.read_csv('sds5_I_reflectance.csv')
df_sds5_K = pd.read_csv('sds5_K_reflectance.csv')
df_sds5_C_stat = pd.read_csv('sds5_C_stat.csv')
df_sds5_H_stat = pd.read_csv('sds5_H_stat.csv')
df_sds5_I_stat = pd.read_csv('sds5_I_stat.csv')
df_sds5_K_stat = pd.read_csv('sds5_K_stat.csv')
df_sds5_C_gray = pd.read_csv('sds5_C_gray.csv')
df_sds5_H_gray = pd.read_csv('sds5_H_gray.csv')
df_sds5_I_gray = pd.read_csv('sds5_I_gray.csv')
df_sds5_K_gray = pd.read_csv('sds5_K_gray.csv')
df_sds7_C = pd.read_csv('sds7_C_reflectance.csv')
df_sds7_H = pd.read_csv('sds7_H_reflectance.csv')
df_sds7_I = pd.read_csv('sds7_I_reflectance.csv')
df_sds7_K = pd.read_csv('sds7_K_reflectance.csv')
df_sds7_C_stat = pd.read_csv('sds7_C_stat.csv')
df_sds7_H_stat = pd.read_csv('sds7_H_stat.csv')
df_sds7_I_stat = pd.read_csv('sds7_I_stat.csv')
df_sds7_K_stat = pd.read_csv('sds7_K_stat.csv')
df_sds7_C_gray = pd.read_csv('sds7_C_gray_interp.csv')
df_sds7_H_gray = pd.read_csv('sds7_H_gray.csv')
df_sds7_I_gray = pd.read_csv('sds7_I_gray.csv')
df_sds7_K_gray = pd.read_csv('sds7_K_gray.csv')
df_sds10_C = pd.read_csv('sds10_C_reflectance.csv')
df_sds10_H = pd.read_csv('sds10_H_reflectance.csv')
df_sds10_I = pd.read_csv('sds10_I_reflectance.csv')
df_sds10_K = pd.read_csv('sds10_K_reflectance.csv')
df_sds10_C_stat = pd.read_csv('sds10_C_stat.csv')
df_sds10_H_stat = pd.read_csv('sds10_H_stat.csv')
df_sds10_I_stat = pd.read_csv('sds10_I_stat.csv')
df_sds10_K_stat = pd.read_csv('sds10_K_stat.csv')
df_sds10_C_gray = pd.read_csv('sds10_C_gray.csv')
df_sds10_H_gray = pd.read_csv('sds10_H_gray.csv')
df_sds10_I_gray = pd.read_csv('sds10_I_gray.csv')
df_sds10_K_gray = pd.read_csv('sds10_K_gray.csv')
df_50um = pd.read_csv('50um_led_interp.csv')
# df_50um = pd.read_csv('50um_led.csv')

df_100um = pd.read_csv('100um_led.csv')
df_200um = pd.read_csv('200um_led.csv')
df_sds5_invivo = pd.read_csv('invivo_sds5.csv')
df_sds7_invivo = pd.read_csv('invivo_sds7.csv')
df_sds10_invivo = pd.read_csv('invivo_sds10.csv')
df_sds5_invivo_ref = pd.read_csv('invivo_sds5_reflectance.csv')
df_sds7_invivo_ref = pd.read_csv('invivo_sds7_reflectance.csv')
df_sds10_invivo_ref = pd.read_csv('invivo_sds10_reflectance.csv')
df_sds5_invivo_stat = pd.read_csv('invivo_sds5_stat.csv')
df_sds7_invivo_stat = pd.read_csv('invivo_sds7_stat.csv')
df_sds10_invivo_stat = pd.read_csv('invivo_sds10_stat.csv')

df_sds10_with_ch2K_stat = pd.read_csv('sds10_ch2K_stat.csv')
df_sds10_with_ch2K_reflectance = pd.read_csv('sds10_ch2K_reflectance.csv')


# %% plot light source spectrum
# plt.figure(dpi=300)
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Intensity (log scale)')
# plt.plot(df_50um.loc[start_wl:stop_wl, 'wl'], np.log(df_50um.loc[start_wl:stop_wl, 'shot_mean']), label='50 um')
# plt.plot(df_100um.loc[start_wl:stop_wl, 'wl'], np.log(df_100um.loc[start_wl:stop_wl, 'shot_mean']), label='100 um')
# plt.plot(df_200um.loc[start_wl:stop_wl, 'wl'], np.log(df_200um.loc[start_wl:stop_wl, 'shot_mean']), label='200 um')
# plt.legend()
# plt.tight_layout()
# plt.savefig('light_source.png')

plt.figure(dpi=300)
plt.title('light source - gray level')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity')
ax = plt.gca()
ax.set_yscale("log")
plt.plot(df_50um.loc[start_wl:stop_wl, 'wl'], (df_50um.loc[start_wl:stop_wl, 'shot_mean']), label='50 um')
plt.plot(df_100um.loc[start_wl:stop_wl, 'wl'], (df_100um.loc[start_wl:stop_wl, 'shot_mean']), label='100 um')
plt.plot(df_200um.loc[start_wl:stop_wl, 'wl'], (df_200um.loc[start_wl:stop_wl, 'shot_mean']), label='200 um')
plt.legend()
plt.tight_layout()
plt.savefig('light_source.png')

# %% plot phamton spectrum
plt.figure(figsize = (16, 8), dpi=300)
plt.xlabel('Wavelength (nm)')
plt.ylabel('CCD count (log scale)')
# plt.ticklabel_format(axis='y', style='sci', scilimits=(1,1))
plt.plot(df_sds5_invivo.loc[start_wl:stop_wl, 'wl'], np.log(df_sds5_invivo.loc[start_wl:stop_wl, 'shot_mean']), linewidth=3,  label='in-vivo, SDS = 5mm, ch1')
plt.plot(df_sds7_invivo.loc[start_wl:stop_wl, 'wl'], np.log(df_sds7_invivo.loc[start_wl:stop_wl, 'shot_mean']), linewidth=3, label='in-vivo, SDS = 7mm, ch2')
plt.plot(df_sds10_invivo.loc[start_wl:stop_wl, 'wl'], np.log(df_sds10_invivo.loc[start_wl:stop_wl, 'shot_mean']), linewidth=3, label='in-vivo, SDS = 10mm, ch3')
plt.plot(df_sds5_C_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds5_C_gray.loc[start_wl:stop_wl, 'shot_mean']), '--', label='Phamton C, SDS = 5mm, ch1')
plt.plot(df_sds5_H_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds5_H_gray.loc[start_wl:stop_wl, 'shot_mean']), '--', label='Phamton H, SDS = 5mm, ch1')
plt.plot(df_sds5_I_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds5_I_gray.loc[start_wl:stop_wl, 'shot_mean']), '--', label='Phamton I, SDS = 5mm, ch1')
plt.plot(df_sds5_K_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds5_K_gray.loc[start_wl:stop_wl, 'shot_mean']), '--', label='Phamton K, SDS = 5mm, ch1')
plt.plot(df_sds7_C_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds7_C_gray.loc[start_wl:stop_wl, 'shot_mean']), '-.', label='Phamton C, SDS = 7mm, ch2')
plt.plot(df_sds7_H_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds7_H_gray.loc[start_wl:stop_wl, 'shot_mean']), '-.', label='Phamton H, SDS = 7mm, ch2')
plt.plot(df_sds7_I_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds7_I_gray.loc[start_wl:stop_wl, 'shot_mean']), '-.', label='Phamton I, SDS = 7mm, ch2')
plt.plot(df_sds7_K_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds7_K_gray.loc[start_wl:stop_wl, 'shot_mean']), '-.', label='Phamton K, SDS = 7mm, ch2')
plt.plot(df_sds10_C_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds10_C_gray.loc[start_wl:stop_wl, 'shot_mean']), ':', label='Phamton C, SDS = 10mm, ch3')
plt.plot(df_sds10_H_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds10_H_gray.loc[start_wl:stop_wl, 'shot_mean']), ':', label='Phamton H, SDS = 10mm, ch3')
plt.plot(df_sds10_I_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds10_I_gray.loc[start_wl:stop_wl, 'shot_mean']), ':', label='Phamton I, SDS = 10mm, ch3')
plt.plot(df_sds10_K_gray.loc[start_wl:stop_wl, 'wl'], np.log(df_sds10_K_gray.loc[start_wl:stop_wl, 'shot_mean']), ':', label='Phamton K, SDS = 10mm, ch3')

plt.legend(loc='best' , bbox_to_anchor=(1,1))
plt.tight_layout()
plt.savefig('all_spec.png')

# %% plot noise pattern 
utility.plotNoise_pattern(df_sds5_H, 'Channel l', 'ch1_noise_pattern.png')
utility.plotNoise_pattern(df_sds7_H, 'Channel 2', 'ch2_noise_pattern.png')
utility.plotNoise_pattern(df_sds10_C, 'Channel 3', 'ch3_noise_pattern.png')

# %% plot cv each channel
plt.figure(dpi=300)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Coefficient of variation ')
x = [700, 720, 740, 760, 780, 800, 820, 840, 860, 880]
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
plt.xticks(x)
plt.yticks(y)

plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
# plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.plot(df_sds5_H_stat['wl'], df_sds5_H_stat['cv']*100, label='SDS = 5 mm')
plt.plot(df_sds7_H_stat['wl'], df_sds7_H_stat['cv']*100, label='SDS = 7 mm')
plt.plot(df_sds10_with_ch2K_stat['wl'], df_sds10_with_ch2K_stat['cv']*100, label='SDS = 10 mm')
plt.legend()
plt.tight_layout()

plt.savefig('cv.png')
# %% write cv each channel to csv
d = {'wl': df_sds5_H_stat['wl'], 'ch1': df_sds5_H_stat['cv'], 'ch2': df_sds7_H_stat['cv'], 'ch3': df_sds10_with_ch2K_stat['cv']}
df = pd.DataFrame(d)
df.to_csv('cv_channel.csv', index=False)

# %% plot invivo spectrum
y_sds5 = df_sds5_invivo_ref.iloc[:, 1:].mean(axis=1)
y_sds7 = df_sds7_invivo_ref.iloc[:, 1:].mean(axis=1)
y_sds10 = df_sds10_invivo_ref.iloc[:, 1:].mean(axis=1)
plt.figure(figsize = (16, 8), dpi=300)
plt.subplot(131)
plt.title('SDS = 5 mm')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized intensity')
plt.plot(df_sds5_invivo_ref.loc[start_wl:stop_wl, 'wl'], y_sds5[start_wl:stop_wl+1])
plt.subplot(132)
plt.title('SDS = 7 mm')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized intensity')
plt.plot(df_sds7_invivo_ref.loc[start_wl:stop_wl, 'wl'], y_sds7[start_wl:stop_wl+1])
plt.subplot(133)
plt.title('SDS = 10 mm')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Normalized intensity')
plt.plot(df_sds10_invivo_ref.loc[start_wl:stop_wl, 'wl'], y_sds10[start_wl:stop_wl+1])
plt.tight_layout()
plt.savefig('invivo.png')

# %% make invivo spec to matlab input
df = pd.DataFrame(np.zeros((stop_wl-start_wl+1, 13)))
df.iloc[:, 0] = df_sds5_invivo_ref.loc[start_wl:stop_wl, 'wl'].values
df.iloc[:, 7] = y_sds5[start_wl:stop_wl+1].values
df.iloc[:, 9] = y_sds7[start_wl:stop_wl+1].values
df.iloc[:, 12] = y_sds10[start_wl:stop_wl+1].values
df.to_csv('invivo.txt', sep='\t', header=False, index=False)
# %%
