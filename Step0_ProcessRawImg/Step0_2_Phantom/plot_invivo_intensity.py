
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# PNAME = '23456CHIK'
# PNAME = ['CC', 'HH', 'II', 'KK']
PNAME = ['22', '33', '44', '55', '66']
invivofolder = 'm_out_20230812_invivo'
invivoname = 'hw_det_mean.csv'
phantomfolder = 'm_out_20230812'
start_id, stop_id = 0, 65
df_invivo = pd.read_csv(os.path.join(invivofolder, invivoname))
df_ph_list = [pd.read_csv(os.path.join(phantomfolder, f'{pid}_det_mean.csv')) for pid in PNAME]
df_invivo_std = pd.read_csv(os.path.join(invivofolder, 'standard-0.04_det_mean.csv'))
df_ph_std = pd.read_csv(os.path.join(phantomfolder, 'standard-0.04_det_mean.csv'))
power_phactor = df_ph_std.iloc[:, 1:].values / df_invivo_std.iloc[:, 1:].values
df_invivo.iloc[:, 1:] *= power_phactor
sds_list = [4.5, 7.5, 10.5]
fig, ax = plt.subplots(1, 3, figsize=(14, 8))
for sds in range(3):
    ax[sds].plot(df_invivo.loc[start_id:stop_id, 'wl'], df_invivo.iloc[start_id:stop_id+1, sds+1], '--', label='In-Vivo')
    for pid, dfph in enumerate(df_ph_list):
        ax[sds].plot(dfph.loc[start_id:stop_id, 'wl'], dfph.iloc[start_id:stop_id+1, sds+1], label=f'Phantom {PNAME[pid]}')
    ax[sds].set_xlabel('Wavelength (nm)')
    ax[sds].set_ylabel('Intensity (counts)')
    ax[sds].set_xticks(np.linspace(700, 880, 10))
    # ax[sds].set_yticks(np.linspace(0, 80000, 6))
    ax[sds].set_title(f'SDS = {sds_list[sds]} mm')
    ax[sds].grid()
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
plt.tight_layout()
plt.savefig(os.path.join('InvivoFigure', 'invivo_intensity_0812.png'))
# plt.show()        
# input('Pause')