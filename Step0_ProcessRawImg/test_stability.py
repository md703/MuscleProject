import numpy as np
import os
import pandas as pd
import skimage.io 
import matplotlib.pyplot as plt
from glob import glob
from tqdm import tqdm
import matplotlib.ticker as mtick

ifolder = 'm_out_20230529-2'
SDS_LIST = [4.5, 7.5, 10.5]
REPEAT_TIMES = 8

font=16
pname = [f'{i}_stability_test_det_mean.csv' for i in np.arange(1, 9, 1, dtype=np.int64)]
fig, ax = plt.subplots(1, 3, figsize=(12, 6))
df_list = 3 * [np.zeros((31, REPEAT_TIMES))]
for i, tar_name in tqdm(enumerate(pname)):
    df = pd.read_csv(os.path.join(ifolder, pname[i]))
    for ch in range(3):
        df_list[ch][:, i] = df[f'ch{ch+1}_mean'] 
    
    # Plot
    for ch in range(3):
        if i == len(pname)-1:
            ax[ch].set_title(f'SDS = {SDS_LIST[ch]} mm', fontsize=font)
            if ch == 1:
                ax[ch].set_xlabel('Wavelength (nm)', fontsize=font)
            if ch == 0:
                ax[ch].set_ylabel('Intensity (counts)', fontsize=font)
            ax[ch].grid(visible=True, linestyle='--')
            wl = df['wl']
        ax[ch].plot(df['wl'], df[f'ch{ch+1}_mean'])
        
fmt = '%.1f%%' # Format you want the ticks, e.g. '40%'
yticks = mtick.FormatStrFormatter(fmt)
# Plot CV
for ch in range(3):
    ax2 = ax[ch].twinx()
    cv = np.std(df_list[ch], axis=1) / np.mean(df_list[ch], axis=1)
    ax2.yaxis.set_major_formatter(yticks)
    ax2.plot(wl, 100 * cv, color='black', linestyle='--')
    ax2.set_yticks(np.linspace(0, 10, 6))
    if ch == 2:
        ax2.set_ylabel('CV', fontsize=font)
    ax2.tick_params(axis='y')

label = [i+1 for i in range(REPEAT_TIMES)]
# fig.legend(labels=label, loc='upper right', bbox_to_anchor=(1.5, 1.))
fig.legend(labels=label, loc='lower right', bbox_to_anchor=(0.9, 0.25), frameon=False, fontsize=font-4)
fig.tight_layout()
fig.savefig(os.path.join(ifolder, 'stability_test.png'), dpi=300)




        