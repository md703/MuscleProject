# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

subject1 = 'hw_20230718_sds_1_2_3_1000k'
subject2 = 'syu_20230626_sds_1_2_3_1000k'

sub = 'HW'
layer = ['epidermis', ]
df_sub1_list = []
df_sub2_list = []

mulist = [('mua1','mus1',0.94,1,'epidermis'), ('mua2','mus2',0.715,2,'dermis'), 
          ('mua3','mus3',0.9,3,'subcu.'), ('mua4', 'mus4',0.93,4,'muscle'),]

for i in range(1, 21):
    df_sub1_list.append(pd.read_csv(os.path.join(subject1, f'fit_all{i}', 'lsqMu_final.csv')))
    df_sub2_list.append(pd.read_csv(os.path.join(subject2, f'fit_all{i}', 'lsqMu_final.csv')))

df_sub_list = df_sub1_list
for muid in mulist:
    fig, ax = plt.subplots(1, 2, figsize=(19.2, 10.8), dpi=300)
    for i in range(len(df_sub_list)):
        ax[0].plot(df_sub_list[i]['wl'], df_sub_list[i][muid[0]])
        ax[1].plot(df_sub_list[i]['wl'], (1-muid[2]) * df_sub_list[i][muid[1]])
    ax[0].set_ylabel('Reflectance', fontsize=20)
    ax[1].set_ylabel('Reflectance', fontsize=20)
    ax[0].yaxis.set_label_coords(-.1, 0.5)
    ax[1].yaxis.set_label_coords(-.1, 0.5)
    ax[0].set_xticks(np.linspace(700, 880, 10))
    ax[1].set_xticks(np.linspace(700, 880, 10))
    ax[0].set_ylim(bottom=0)
    ax[1].set_ylim(bottom=0)
    ax[0].set_xlabel('Wavelength (nm)', fontsize=20)
    ax[1].set_xlabel('Wavelength (nm)', fontsize=20)
    ax[0].set_ylabel('μ$_{a}$ (cm$^{-1}$)', fontsize=20)
    ax[1].set_ylabel('μ$_{s}$\' (cm$^{-1}$)', fontsize=20)
    ax[0].tick_params(axis='both', which='major', labelsize=14)
    ax[1].tick_params(axis='both', which='major', labelsize=14)
    ax[0].xaxis.set_label_coords(.5, -.05)
    ax[1].xaxis.set_label_coords(.5, -.05)
    ax[0].grid(linestyle=':')
    ax[1].grid(linestyle=':')
    box = ax[0].get_position()
    ax[0].set_position([box.x0 - box.width*0.1, box.y0,
                 box.width, box.height])
    box = ax[1].get_position()
    ax[1].set_position([box.x0 + box.width*0.1, box.y0,
                 box.width, box.height])
    fig.suptitle(f'20 fits, {muid[4]}', fontsize=26)
    fig.savefig(f'twenty_fit_mu{muid[3]}.png')
pass