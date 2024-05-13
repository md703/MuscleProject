# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots

# plt.style.use(['science', 'nature'])

subject1 = 'hw_20230718_sds_1_2_3'

df_mua1 = pd.read_csv('data/mua_epi.csv').dropna(axis=0, how='all')
df_mua2 = pd.read_csv('data/mua_dermis.csv').dropna(axis=0, how='all')  
df_mua3 = pd.read_csv('data/mua_subcu.csv').dropna(axis=0, how='all')
df_mua4 = pd.read_csv('data/mua_muscle.csv').dropna(axis=0, how='all')
df_musp1 = pd.read_csv('data/musp_epi.csv').dropna(axis=0, how='all')
df_musp2 = pd.read_csv('data/musp_dermis.csv').dropna(axis=0, how='all')
df_musp3 = pd.read_csv('data/musp_subcu.csv').dropna(axis=0, how='all')
df_musp4 = pd.read_csv('data/musp_muscle.csv').dropna(axis=0, how='all')

df_sub1 = pd.read_csv(os.path.join(subject1, 'fit_all4', 'lsqMu_final.csv'))
wl = df_mua1['wl'].values
wl = wl[0:: 20]
legend_size = 16
label_size = 26
tick_size = 20
line_width = 1
# # %% Plot epidermis OPs 
# fig, ax = plt.subplots(1, 2, dpi=300)
# ax[0].plot(wl, df_mua1.loc[::20, 'Marchesini 1992'], '#D2691E', marker='s', markerfacecolor='none', label='Marchesini 1992, IMC')
# ax[0].plot(wl, df_mua1.loc[::20, 'Salomatina 2006'], 'r', marker='s', markerfacecolor='none', label='Salomatina 2006, IMC')
# ax[0].plot(wl, df_mua1.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='s', markerfacecolor='none', label='Shimojo 2020, IMC, Asian')
# ax[0].plot(df_sub1['wl'], df_sub1['mua1'], 'k--', marker='s', label='Subject HW')

# ax[1].plot(wl, df_musp1.loc[::20, 'Marchesini 1992'], '#D2691E', marker='s', markerfacecolor='none', label='Marchesini 1992, IMC')
# ax[1].plot(wl, df_musp1.loc[::20, 'Salomatina 2006'], 'r', marker='s', markerfacecolor='none', label='Salomatina 2006, IMC')
# ax[1].plot(wl, df_musp1.loc[::20, '(in-vivo) Jonasson 2018'], '#800080', marker='s', markerfacecolor='none', label='Jonasson 2018, IMC, $\it{in}$ $\it{vivo}$')
# ax[1].plot(wl, df_musp1.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='s', markerfacecolor='none', label='Shimojo 2020, IMC, Asian')
# ax[1].plot(df_sub1['wl'], 0.06*df_sub1['mus1'], 'k--', marker='s', label='Subject HW')

# # %% Plot dermis OPs 
# ax[0].plot(wl, df_mua2.loc[::20, 'Simpson 1998 caucasian skin'], '#00FF00', marker='d', markerfacecolor='none', label='Simpson 1998 caucasian skin, IMC')
# ax[0].plot(wl, df_mua2.loc[::20, 'Simpson 1998 negroid skin'], '#008000', marker='d', markerfacecolor='none', label='Simpson 1998 negroid skin, IMC')
# ax[0].plot(wl, df_mua2.loc[::20, 'Bashkatov 2005 skin'], '#FFA500', marker='d', markerfacecolor='none', label='Bashkatov 2005 skin, IAD')
# ax[0].plot(wl, df_mua2.loc[::20, 'Salomatina 2006 dermis'], 'r', marker='d', markerfacecolor='none', label='Salomatina 2006 dermis, IMC')
# ax[0].plot(wl, df_mua2.loc[::20, 'Shimojo 2020 Asian dermis'], 'b', marker='d', markerfacecolor='none', label='Shimojo 2020 dermis, IMC, Asian')
# ax[0].plot(df_sub1['wl'], df_sub1['mua2'], 'k--', marker='d', label='Subject HW')
    
# ax[1].plot(wl, df_musp2.loc[::20, 'Simpson 1998 caucasian skin'], '#00FF00', marker='d', markerfacecolor='none', label='Simpson 1998 caucasian skin, IMC')
# ax[1].plot(wl, df_musp2.loc[::20, 'Simpson 1998 negroid skin'], '#008000', marker='d', markerfacecolor='none', label='Simpson 1998 negroid skin, IMC')
# ax[1].plot(wl, df_musp2.loc[::20, 'Bashkatov 2005 skin'], '#FFA500', marker='d', markerfacecolor='none', label='Bashkatov 2005 skin, IAD')
# ax[1].plot(wl, df_musp2.loc[::20, 'Salomatina 2006 dermis'], 'r', marker='d', markerfacecolor='none', label='Salomatina 2006 dermis, IMC')
# ax[1].plot(wl, df_musp2.loc[::20, 'Shimojo 2020 Asian dermis'], 'b', marker='d', markerfacecolor='none', label='Shimojo 2020 dermis, IMC, Asian')
# ax[1].plot(df_sub1['wl'], 0.285*df_sub1['mus2'], 'k--', marker='d', label='Subject HW')

# # %% Plot subcu. OPs 
# ax[0].plot(wl, df_mua3.loc[::20, 'Simpson 1998'], '#00FF00', marker='o', markerfacecolor='none', label='Simpson 1998, IMC')
# ax[0].plot(wl, df_mua3.loc[::20, 'Bashkatov 2005'], '#FFA500', marker='o', markerfacecolor='none', label='Bashkatov 2005, IAD')
# ax[0].plot(wl, df_mua3.loc[::20, 'Salomatina 2006'], 'r', marker='o', markerfacecolor='none', label='Salomatina 2006, IMC')
# ax[0].plot(wl, df_mua3.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='o', markerfacecolor='none', label='Shimojo 2020, IMC, Asian')
# ax[0].plot(df_sub1['wl'], df_sub1['mua3'], 'k--', marker='o', label='Subject HW')

# ax[1].plot(wl, df_musp3.loc[::20, 'Simpson 1998'], '#00FF00', marker='o', markerfacecolor='none', label='Simpson 1998, IMC')
# ax[1].plot(wl, df_musp3.loc[::20, 'Bashkatov 2005'], '#FFA500', marker='o', markerfacecolor='none', label='Bashkatov 2005, IAD')
# ax[1].plot(wl, df_musp3.loc[::20, 'Salomatina 2006'], 'r', marker='o', markerfacecolor='none', label='Salomatina 2006, IMC')
# ax[1].plot(wl, df_musp3.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='o', markerfacecolor='none', label='Shimojo 2020, IMC, Asian')
# ax[1].plot(df_sub1['wl'], 0.1*df_sub1['mus3'], 'k--', marker='o', label='Subject HW')

# # %% Plot muscle. OPs 
# ax[0].plot(wl, df_mua4.loc[::20, '(Rat)Nilsson 1995'], '#F0E68C', marker='*', markerfacecolor='none', label='Nilsson 1995, IMC, Rat')
# ax[0].plot(wl, df_mua4.loc[::20, 'Simpson 1998'], '#00FF00', marker='*', markerfacecolor='none', label='Simpson 1998, IMC')
# ax[0].plot(wl, df_mua4.loc[::20, '(Beef)Xia, Jinjun 2006'], '#FFC0CB', marker='*', markerfacecolor='none', label='Jinjun 2006, Diffusion theory, Beef')
# ax[0].plot(df_sub1['wl'], df_sub1['mua4'], 'k--', marker='*', label='Subject HW')

# ax[1].plot(wl, df_musp4.loc[::20, '(Rat)Nilsson 1995'], '#F0E68C', marker='*', markerfacecolor='none', label='Nilsson 1995, IMC, Rat')
# ax[1].plot(wl, df_musp4.loc[::20, 'Simpson 1998'], '#00FF00', marker='*', markerfacecolor='none', label='Simpson 1998, IMC')
# ax[1].plot(wl, df_musp4.loc[::20, '(Beef)Xia, Jinjun 2006'], '#FFC0CB', marker='*', markerfacecolor='none', label='Jinjun 2006, Diffusion theory, Beef')
# ax[1].plot(df_sub1['wl'], 0.07*df_sub1['mus4'], 'k--', marker='*', label='Subject HW')

# ax[0].set_xticks(np.linspace(700, 880, 10))
# ax[0].set_ylim(bottom=0)
# ax[0].set_xlabel('Wavelength (nm)')
# ax[0].set_ylabel('μ$_{a}$ (cm$^{-1}$)')
# ax[0].tick_params(axis='both', which='major')
# ax[0].yaxis.set_label_coords(-.125, 0.5)
# ax[0].xaxis.set_label_coords(.5, -.05)
# box = ax[0].get_position()
# ax[0].set_position([box.x0 - box.width*0.1, box.y0 + box.height * 0.15,
#                  box.width, box.height * 0.9])
# ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 0),
#           edgecolor='black', ncol=2)
# ax[0].grid(linestyle=':')

# ax[1].set_xticks(np.linspace(700, 880, 10))
# ax[1].set_ylim(bottom=0)
# ax[1].set_xlabel('Wavelength (nm)')
# ax[1].set_ylabel('μ$_{s}$\' (cm$^{-1}$)')
# ax[1].tick_params(axis='both', which='major')
# ax[1].yaxis.set_label_coords(-.1, 0.5)
# ax[1].xaxis.set_label_coords(.5, -.05)
# box = ax[1].get_position()
# ax[1].set_position([box.x0 + box.width*0.1, box.y0 + box.height * 0.15,
#                  box.width, box.height * 0.9])
# ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, 0),
#           edgecolor='black', ncol=2)
# ax[1].grid(linestyle=':')

# fig.savefig('all_op.png')
# %% Plot epidermis OPs 
fig, ax = plt.subplots(1, 2, figsize=(30, 8), dpi=300)
ax[0].plot(wl, df_mua1.loc[::20, 'Marchesini 1992'], '#D2691E', marker='s', markerfacecolor='none', label='Marchesini 1992, IMC, epidermis')
ax[0].plot(wl, df_mua1.loc[::20, 'Salomatina 2006'], 'r', marker='s', markerfacecolor='none', label='Salomatina 2006, IMC, epidermis')
ax[0].plot(wl, df_mua1.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='s', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, epidermis')
ax[0].plot(df_sub1['wl'], df_sub1['mua1'], 'k--', marker='s', label='Subject 1, epidermis')

ax[1].plot(wl, df_musp1.loc[::20, 'Marchesini 1992'], '#D2691E', marker='s', markerfacecolor='none', label='Marchesini 1992, IMC, epidermis')
ax[1].plot(wl, df_musp1.loc[::20, 'Salomatina 2006'], 'r', marker='s', markerfacecolor='none', label='Salomatina 2006, IMC, epidermis')
ax[1].plot(wl, df_musp1.loc[::20, '(in-vivo) Jonasson 2018'], '#800080', marker='s', markerfacecolor='none', label='Jonasson 2018, IMC, $\it{in}$ $\it{vivo}$, epidermis')
ax[1].plot(wl, df_musp1.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='s', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, epidermis')
ax[1].plot(df_sub1['wl'], 0.06*df_sub1['mus1'], 'k--', marker='s', label='Subject 1, epidermis')

# %% Plot dermis OPs 
ax[0].plot(wl, df_mua2.loc[::20, 'Simpson 1998 caucasian skin'], '#00FF00', marker='d', markerfacecolor='none', label='Simpson 1998 caucasian, IMC, skin')
ax[0].plot(wl, df_mua2.loc[::20, 'Simpson 1998 negroid skin'], '#008000', marker='d', markerfacecolor='none', label='Simpson 1998 negroid, IMC, skin')
ax[0].plot(wl, df_mua2.loc[::20, 'Bashkatov 2005 skin'], '#FFA500', marker='d', markerfacecolor='none', label='Bashkatov 2005, IAD, skin')
ax[0].plot(wl, df_mua2.loc[::20, 'Salomatina 2006 dermis'], 'r', marker='d', markerfacecolor='none', label='Salomatina 2006, IMC, dermis')
ax[0].plot(wl, df_mua2.loc[::20, 'Shimojo 2020 Asian dermis'], 'b', marker='d', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, dermis')
ax[0].plot(df_sub1['wl'], df_sub1['mua2'], 'k--', marker='d', label='Subject 1, dermis')
    
ax[1].plot(wl, df_musp2.loc[::20, 'Simpson 1998 caucasian skin'], '#00FF00', marker='d', markerfacecolor='none', label='Simpson 1998 caucasian, IMC, skin')
ax[1].plot(wl, df_musp2.loc[::20, 'Simpson 1998 negroid skin'], '#008000', marker='d', markerfacecolor='none', label='Simpson 1998 negroid, IMC, skin')
ax[1].plot(wl, df_musp2.loc[::20, 'Bashkatov 2005 skin'], '#FFA500', marker='d', markerfacecolor='none', label='Bashkatov 2005, IAD, skin')
ax[1].plot(wl, df_musp2.loc[::20, 'Salomatina 2006 dermis'], 'r', marker='d', markerfacecolor='none', label='Salomatina 2006, IMC, dermis')
ax[1].plot(wl, df_musp2.loc[::20, 'Shimojo 2020 Asian dermis'], 'b', marker='d', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, dermis')
ax[1].plot(df_sub1['wl'], 0.285*df_sub1['mus2'], 'k--', marker='d', label='Subject 1, dermis')

# %% Plot subcu. OPs 
ax[0].plot(wl, df_mua3.loc[::20, 'Simpson 1998'], '#00FF00', marker='o', markerfacecolor='none', label='Simpson 1998, IMC, subcu.')
ax[0].plot(wl, df_mua3.loc[::20, 'Bashkatov 2005'], '#FFA500', marker='o', markerfacecolor='none', label='Bashkatov 2005, IAD, subcu.')
ax[0].plot(wl, df_mua3.loc[::20, 'Salomatina 2006'], 'r', marker='o', markerfacecolor='none', label='Salomatina 2006, IMC, subcu.')
ax[0].plot(wl, df_mua3.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='o', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, subcu.')
ax[0].plot(df_sub1['wl'], df_sub1['mua3'], 'k--', marker='o', label='Subject 1, subcu.')

ax[1].plot(wl, df_musp3.loc[::20, 'Simpson 1998'], '#00FF00', marker='o', markerfacecolor='none', label='Simpson 1998, IMC, subcu.')
ax[1].plot(wl, df_musp3.loc[::20, 'Bashkatov 2005'], '#FFA500', marker='o', markerfacecolor='none', label='Bashkatov 2005, IAD, subcu.')
ax[1].plot(wl, df_musp3.loc[::20, 'Salomatina 2006'], 'r', marker='o', markerfacecolor='none', label='Salomatina 2006, IMC, subcu.')
ax[1].plot(wl, df_musp3.loc[::20, 'Shimojo 2020 Asian'], 'b', marker='o', markerfacecolor='none', label='Shimojo 2020, IMC, Asian, subcu.')
ax[1].plot(df_sub1['wl'], 0.1*df_sub1['mus3'], 'k--', marker='o', label='Subject 1, subcu.')

# %% Plot muscle. OPs 
ax[0].plot(wl, df_mua4.loc[::20, '(Rat)Nilsson 1995'], '#F0E68C', marker='*', markerfacecolor='none', label='Nilsson 1995, IMC, Rat, muscle')
ax[0].plot(wl, df_mua4.loc[::20, 'Simpson 1998'], '#00FF00', marker='*', markerfacecolor='none', label='Simpson 1998, IMC, muscle')
ax[0].plot(wl, df_mua4.loc[::20, '(Beef)Xia, Jinjun 2006'], '#FFC0CB', marker='*', markerfacecolor='none', label='Jinjun 2006, Diffusion theory, Beef, muscle')
ax[0].plot(df_sub1['wl'], df_sub1['mua4'], 'k--', marker='*', label='Subject 1, muscle')

ax[1].plot(wl, df_musp4.loc[::20, '(Rat)Nilsson 1995'], '#F0E68C', marker='*', markerfacecolor='none', label='Nilsson 1995, IMC, Rat, muscle')
ax[1].plot(wl, df_musp4.loc[::20, 'Simpson 1998'], '#00FF00', marker='*', markerfacecolor='none', label='Simpson 1998, IMC, muscle')
ax[1].plot(wl, df_musp4.loc[::20, '(Beef)Xia, Jinjun 2006'], '#FFC0CB', marker='*', markerfacecolor='none', label='Jinjun 2006, Diffusion theory, Beef, muscle')
ax[1].plot(df_sub1['wl'], 0.07*df_sub1['mus4'], 'k--', marker='*', label='Subject 1, muscle')

ax[0].set_yscale('log')
ax[0].set_xticks(np.linspace(700, 880, 5))
ax[0].set_yticks([0.1, 1, 10])
ax[0].set_ylim(bottom=0)
ax[0].set_xlabel('Wavelength (nm)', fontsize=label_size)
ax[0].set_ylabel('μ$_{a}$ (cm$^{-1}$)', fontsize=label_size)
ax[0].tick_params(axis='both', which='major', labelsize=tick_size)
# ax[0].yaxis.set_label_coords(-.125, 0.5)
# ax[0].xaxis.set_label_coords(.5, -.05)
box = ax[0].get_position()
ax[0].set_position([box.x0 + box.width*0.5, box.y0,
                 box.width*0.5, box.height])
ax[0].legend(bbox_to_anchor=(-0.2, 1),
          edgecolor='none', frameon=False, fontsize=legend_size, ncol=1)
# ax[0].legend(loc='best',  
#           edgecolor='none', frameon=False, fontsize=legend_size, ncol=2)
ax[0].grid(linestyle=':')

ax[1].set_yscale('log')
ax[1].set_xticks(np.linspace(700, 880, 5))
ax[1].set_yticks([1, 10, 100])
ax[1].set_ylim(bottom=0)
ax[1].set_xlabel('Wavelength (nm)', fontsize=label_size)
ax[1].set_ylabel('μ$_{s}$\' (cm$^{-1}$)', fontsize=label_size)
ax[1].tick_params(axis='both', which='major', labelsize=tick_size)
# ax[1].yaxis.set_label_coords(-.1, 0.5)
# ax[1].xaxis.set_label_coords(.5, -.05)
box = ax[1].get_position()
ax[1].set_position([box.x0, box.y0,
                 box.width*0.5, box.height])
ax[1].legend(bbox_to_anchor=(1, 1), frameon=False, fontsize=legend_size,
          edgecolor='none', ncol=1)
# ax[1].legend(loc='best',
#           edgecolor='none', frameon=False, fontsize=legend_size, ncol=2)
ax[1].grid(linestyle=':')
# plt.show()
# fig.tight_layout()
fig.savefig('all_op.png')
