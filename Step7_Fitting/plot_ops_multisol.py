import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
from glob import glob
from natsort import natsorted
from tqdm import tqdm


subject = 'by'
path = 'by_test'
title = 'by 1106'
font = 13
path2 = glob(os.path.join(path, '*'))
path2 = path2[0]
choose_id = [i for i in range(1, 21)]

# fit_wl =  np.array([711,716,724,732,755,759,763,769,779,788,798,805,812,820,826,832,840,854,866,880])
# fit_wl = np.array([700, 708, 716, 724, 732, 739, 742, 745, 752, 755, 757, 759, 761, 763, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
# tar_wl = np.arange(680, 901)

fig1, ax1 = plt.subplots(2, 2, figsize=(10, 8))
fig2, ax2 = plt.subplots(2, 2, figsize=(10, 8))

for id in choose_id:
    mupath = os.path.join(path2, f'fit_all{id}', 'lsqMu_final.csv')
    df = pd.read_csv(mupath)
    ax1[0, 0].plot(df['wl'], df['mua1'], label=str(id))
    ax1[0, 1].plot(df['wl'], df['mua2'], label=str(id))
    ax1[1, 0].plot(df['wl'], df['mua3'], label=str(id))
    ax1[1, 1].plot(df['wl'], df['mua4'], label=str(id))
    ax2[0, 0].plot(df['wl'], df['mus1']*0.06, label=str(id))
    ax2[0, 1].plot(df['wl'], df['mus2']*0.285, label=str(id))
    ax2[1, 0].plot(df['wl'], df['mus3']*0.1, label=str(id))
    ax2[1, 1].plot(df['wl'], df['mus4']*0.1, label=str(id))
ax1[0, 0].set_title('epidermis mua')
ax1[0, 1].set_title('dermis mua')
ax1[1, 0].set_title('subcu. mua')
ax1[1, 1].set_title('muscle mua')
ax2[0, 0].set_title('epidermis musp')
ax2[0, 1].set_title('dermis musp')
ax2[1, 0].set_title('subcu. musp')
ax2[1, 1].set_title('muscle musp')
ax1[1, 0].set_xlabel('Wavelength (nm)')
ax1[1, 1].set_xlabel('Wavelength (nm)')
ax2[1, 0].set_xlabel('Wavelength (nm)')
ax2[1, 1].set_xlabel('Wavelength (nm)')
ax1[0, 0].set_ylabel('$\mu_a$ ($cm^{-1}$)')
ax1[1, 0].set_ylabel('$\mu_a$ ($cm^{-1}$)')
ax2[0, 0].set_ylabel('$\mu_s$ ($cm^{-1}$)')
ax2[1, 0].set_ylabel('$\mu_s$ ($cm^{-1}$)')
ax1[0, 0].grid(linestyle='--')
ax1[0, 1].grid(linestyle='--')
ax1[1, 0].grid(linestyle='--')
ax1[1, 1].grid(linestyle='--')
ax2[0, 0].grid(linestyle='--')
ax2[0, 1].grid(linestyle='--')
ax2[1, 0].grid(linestyle='--')
ax2[1, 1].grid(linestyle='--')
ax1[0, 1].legend(frameon=False, bbox_to_anchor=(1.2, 1))
ax2[0, 1].legend(frameon=False, bbox_to_anchor=(1.2, 1))

for i in range(2):
    for j in range(2):
        ax1[i, j].set_xticks(np.linspace(700, 880, 7))
        ax2[i, j].set_xticks(np.linspace(700, 880, 7))
        ax1[i, j].set_ylim(bottom=0)
        ax2[i, j].set_ylim(bottom=0)

fig1.tight_layout()    
fig2.tight_layout()    
fig1.savefig(os.path.join(path2, f'{subject}_neck_mua.png'), dpi=300)
fig2.savefig(os.path.join(path2, f'{subject}_neck_mus.png'), dpi=300)
