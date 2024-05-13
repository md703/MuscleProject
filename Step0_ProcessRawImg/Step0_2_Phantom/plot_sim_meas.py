"""
This script plot both simulated and measured spectra, whitch can
check if they were consistence
Input: simulated spectra, measured spectra
Output: figure of simulated spectra & measured spectra
"""

import os 
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime

dt = datetime.now()
dstring = dt.strftime('%Y%m%d-%H-%M-%S')

PNAME = '3456'
SDS_LIST = [4.56, 7.49, 10.55]
simpath = 's_out_1e9_fiber3_3456_new'
measpath = 'm_out_fiber3_20230503'
ofolder = 'plot_' + dstring + '_fiber3'
os.mkdir(ofolder)

for pid in PNAME:
    df_meas1 = pd.read_csv(os.path.join(measpath, f'{pid}_reflectance_ch1.csv'))
    df_meas2 = pd.read_csv(os.path.join(measpath, f'{pid}_reflectance_ch2.csv'))
    df_meas3 = pd.read_csv(os.path.join(measpath, f'{pid}_reflectance_ch3.csv'))
    df_sim = pd.read_csv(os.path.join(simpath, f'norm_spec_{pid}.csv'))
    d = {'wl': df_meas1['wl'].values,
         'ch1': np.mean(df_meas1.loc[:, 'shot_0':], 1),
         'ch2': np.mean(df_meas2.loc[:, 'shot_0':], 1),
         'ch3': np.mean(df_meas3.loc[:, 'shot_0':], 1)}
    df_meas = pd.DataFrame(d)
    fig, ax = plt.subplots(1, 3, figsize=(12, 6), dpi=300)
    for i, sds in enumerate(range(len(SDS_LIST))):
        ax[sds].plot(df_sim['wl'], df_sim[f'ch{sds+1}'])
        ax[sds].plot(df_meas['wl'], df_meas[f'ch{sds+1}'])
        ax[sds].set_xticks(np.arange(700, 881, 30))
        if sds == 0:
            # ax[sds].set_yticks(np.linspace(0, 1.5, 6))
            # ax[sds].set_yticks(np.linspace(0, 8, 6))
            ax[sds].set_yticks(np.linspace(0, 35, 6))
        elif sds == 1:
            # ax[sds].set_yticks(np.linspace(0, 1.2, 6))
            # ax[sds].set_yticks(np.linspace(0, 1.4, 6))
            ax[sds].set_yticks(np.linspace(0, 10, 6))
        elif sds == 2:
            # ax[sds].set_yticks(np.linspace(0, 0.2, 7))
            # ax[sds].set_yticks(np.linspace(0, 0.5, 7))
            ax[sds].set_yticks(np.linspace(0, 1.5, 7))
        ax[sds].set_xlabel('Wavelength [nm]')
        ax[sds].set_ylabel('Normalized Intensity [-]')
        ax[sds].grid(visible=True)
        if sds == len(SDS_LIST)-1:
            labels=['Simulation', 'Measured']
            ax[sds].legend(labels, loc='upper right', bbox_to_anchor=(1.5, 1.) )
    
        # Calculate RMSP
        wl = df_sim['wl']
        tar = np.interp(wl, df_meas.loc[:, 'wl'], df_meas.loc[:, f'ch{i+1}'])
        sim = df_sim.loc[:, f'ch{i+1}']
        rmsp = 100 * np.sqrt(np.sum(((sim-tar)/tar)**2) / tar.size)
        ax[sds].set_title(f'SDS = {SDS_LIST[sds]} [mm], RMSPE = {rmsp:>.1f}%')
        # plt.show()
    
    fig.suptitle(f'Phantom {pid}')
    fig.tight_layout()
    fig.savefig(os.path.join(ofolder, f'{pid}.png'))
    
fiber_diameter = ['50', '105', '200']

# Plot led spectra
df_led = pd.read_csv(os.path.join(measpath, 'led_mean.csv'))
fig, ax = plt.subplots(3, 1, figsize=(6, 8), dpi=300)
for sds in range(len(SDS_LIST)):
    ax[sds].set_xticks(np.arange(700, 881, 30))
    ax[sds].set_xlabel('Wavelength [nm]')
    ax[sds].set_ylabel('Gray value [-]')
    ax[sds].set_title(f'{fiber_diameter[sds]} μm')
    ax[sds].grid(visible=True)
    ax[sds].plot(df_led['wl'], df_led[f'ch{sds+1}_mean'])
fig.tight_layout()
fig.savefig(os.path.join(ofolder, 'led.png'))
print('Finished !\n')