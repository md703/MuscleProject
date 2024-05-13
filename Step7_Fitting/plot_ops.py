# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from brokenaxes import brokenaxes

def set_axes(ax, ylabel_name, type):
    legend_size = 16
    label_size = 20
    tick_size = 15
    line_width = 1.5
    ax.set_xticks(np.linspace(700, 880, 7))
    ax.set_xlim(right=880)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('Wavelength (nm)', fontsize=label_size+2)
    ax.set_ylabel(ylabel_name, fontsize=label_size+2)
    ax.tick_params(axis='both', which='major', labelsize=tick_size)
    box = ax.get_position()
    ax.xaxis.set_label_coords(.5, -.05)
    ax.yaxis.set_label_coords(-.1, 0.5)
    if type == 'mua':
        ax.set_position([box.x0 - box.width*0.1, box.y0 + box.height * 0.25,
                    box.width, box.height * 0.8])
    elif type == 'mus':
        ax.set_position([box.x0 + box.width*0.08, box.y0 + box.height * 0.25,
                    box.width, box.height * 0.8])
    
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
            edgecolor='black', ncol=2, fontsize=legend_size, frameon=False)
    ax.grid(linestyle=':')
    return ax
subject1 = 'kb_test/20231026_kb_sr2_sds_1_2_3'

subject2 = 'eu_test/20231016_eu_sr2_sds_1_2_3'
subject3 = 'by_test/20231016_by_sr2_sds_1_2_3'

df_mua1 = pd.read_csv('data/mua_epi.csv')
df_mua2 = pd.read_csv('data/mua_dermis.csv')  
df_mua3 = pd.read_csv('data/mua_subcu.csv')
df_mua4 = pd.read_csv('data/mua_muscle.csv')
df_musp1 = pd.read_csv('data/musp_epi.csv')
df_musp2 = pd.read_csv('data/musp_dermis.csv')
df_musp3 = pd.read_csv('data/musp_subcu.csv')
df_musp4 = pd.read_csv('data/musp_muscle.csv')

plotSub1 = True
plotSub2 = True
plotSub3 = True

sub1_list = []
sub2_list = []
sub3_list = []
for i in range(1, 21, 1):
    df_sub1 = pd.read_csv(os.path.join(subject1, f'fit_all{i}', 'lsqMu_final.csv'))
    sub1_list.append(df_sub1)
for i in range(1, 21, 1):
    df_sub2 = pd.read_csv(os.path.join(subject2, f'fit_all{i}', 'lsqMu_final.csv'))
    sub2_list.append(df_sub2)
for i in range(1, 21, 1):
    df_sub3 = pd.read_csv(os.path.join(subject3, f'fit_all{i}', 'lsqMu_final.csv'))
    sub3_list.append(df_sub3)
# sub1plot_index = [2,19]
sub1plot_index = [2]
# sub2plot_index = [6,8]
sub2plot_index = [6]
# sub3plot_index = [i for i in range(1, 21, 1)]
sub3plot_index = [12,16, 18]
    
legend_size = 16
label_size = 20
tick_size = 15
line_width = 1.5
marker = ['o', 'v', '^', '<', '>', 's', 'p', '+', 'x', '*']*2
# %% Plot epidermis OPs 
fig, ax = plt.subplots(1, 2, figsize=(22, 12), dpi=300)
# ax[0].plot(df_mua1['wl'], 0.01*df_mua1['Marchesini 1992'], '--', linewidth=line_width, label='R. Marchesini et al.', color='tab:pink')
# # ax[0].fill_between(df_mua1['wl'], 0.01*(df_mua1['Marchesini 1992']-2*df_mua1['Marchesini_l']), 0.01*(df_mua1['Marchesini 1992']+2*df_mua1['Marchesini_u']), alpha=0.5, edgecolor='tab:pink',facecolor='tab:pink')
# # ax[0].errorbar(df_mua1['wl'], 0.01*df_mua1['Marchesini 1992'], yerr=(0.01*(2*df_mua1['Marchesini_l']), 0.01*(2*df_mua1['Marchesini_u'])))
# ax[0].plot(df_mua1['wl'], 0.01*df_mua1['Salomatina 2006'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[0].fill_between(df_mua1['wl'], 0.01*(df_mua1['Salomatina 2006']-2*df_mua1['Salomatina_std']), 0.01*(df_mua1['Salomatina 2006']+2*df_mua1['Salomatina_std']), alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[0].plot(df_mua1['wl'], 0.01*df_mua1['Shimojo 2020 Asian'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[0].fill_between(df_mua1['wl'], 0.01*(df_mua1['Shimojo 2020 Asian']-2*df_mua1['Shimojo_std']), 0.01*(df_mua1['Shimojo 2020 Asian']+2*df_mua1['Shimojo_std']), alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[0].plot(df_mua1['wl'], 0.01*(df_mua1['D. Yudovsky_lb']+df_mua1['D. Yudovsky_ub'])/2, ':', linewidth=line_width, label='D. Yudovsky et al', color='tab:green')
# # ax[0].fill_between(df_mua1['wl'], 0.01*df_mua1['D. Yudovsky_lb'], 0.01*df_mua1['D. Yudovsky_ub'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[0].plot(df_mua1['wl'], 0.01*(df_mua1['D. Yudovsky, A. J. Durkin_lb']+df_mua1['D. Yudovsky, A. J. Durkin_ub'])/2, ':', linewidth=line_width, label='D. Yudovsky, A. J. Durkin', color='tab:red')
# # ax[0].fill_between(df_mua1['wl'], 0.01*df_mua1['D. Yudovsky, A. J. Durkin_lb'], 0.01*df_mua1['D. Yudovsky, A. J. Durkin_ub'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[0].plot(df_mua1['wl'], 0.01*(df_mua1['S.-Y. Tsui_lb']+df_mua1['S.-Y. Tsui_ub'])/2, ':', linewidth=line_width, label='S.-Y. Tsui et al.', color='tab:purple')
# # ax[0].fill_between(df_mua1['wl'], 0.01*df_mua1['S.-Y. Tsui_lb'], 0.01*df_mua1['S.-Y. Tsui_ub'], alpha=0.5, edgecolor='tab:purple',facecolor='tab:purple')
# ax[0].plot(df_mua1['wl'], 0.01*(df_mua1['C.-Y. Wang_lb']+df_mua1['C.-Y. Wang_ub'])/2, ':', linewidth=line_width, label='C.-Y. Wang et al.', color='tab:brown')
# # ax[0].fill_between(df_mua1['wl'], 0.01*df_mua1['C.-Y. Wang_lb'], 0.01*df_mua1['C.-Y. Wang_ub'], alpha=0.5, edgecolor='tab:brown',facecolor='tab:brown')
# ax[0].plot(df_mua1['wl'], df_mua1['H. Jonasson et al. 2023'], ':', linewidth=line_width, label='H. Jonasson et al. 2023', color='tab:orange')
# # ax[0].fill_between(df_mua1['wl'], df_mua1['H. Jonasson et al. 2023_lb'], df_mua1['H. Jonasson et al. 2023_ub'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[0].plot(df_sub1['wl'], 0.01*df_sub1['mua1'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[0].plot(df_sub2['wl'], 0.01*df_sub2['mua1'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[0].plot(df_sub3['wl'], 0.01*df_sub3['mua1'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')


ylabel_name = '$thick \ × \ μ_{a} (-)$'
ax[0] = set_axes(ax[0], ylabel_name, 'mua')


# ax[1].plot(df_musp1['wl'], df_musp1['Marchesini 1992'], '--', linewidth=line_width, label='R. Marchesini et al.', color='tab:pink')
# # ax[1].fill_between(df_musp1['wl'], df_musp1['Marchesini 1992']-2*df_musp1['Marchesini_std'], df_musp1['Marchesini 1992']+2*df_musp1['Marchesini_std'], alpha=0.5, edgecolor='tab:pink',facecolor='tab:pink')
# ax[1].plot(df_musp1['wl'], df_musp1['Salomatina 2006'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[1].fill_between(df_musp1['wl'], df_musp1['Salomatina 2006']-2*df_musp1['Salomatina_std'], df_musp1['Salomatina 2006']+2*df_musp1['Salomatina_std'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[1].plot(df_musp1['wl'], df_musp1['Shimojo 2020 Asian'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[1].fill_between(df_musp1['wl'], df_musp1['Shimojo 2020 Asian']-2*df_musp1['Shimojo_std'], df_musp1['Shimojo 2020 Asian']+2*df_musp1['Shimojo_std'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[1].plot(df_sub1['wl'], 0.06*df_sub1['mus1'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[1].plot(df_sub2['wl'], 0.06*df_sub2['mus1'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[1].plot(df_sub3['wl'], 0.06*df_sub3['mus1'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')


ylabel_name = '$μ_{s}$\' ($cm^{-1}$)'
ax[1] = set_axes(ax[1], ylabel_name, 'mus')

fig.suptitle('Epidermis', fontsize=label_size+4)
# fig.savefig('op1_res.png', transparent=True)
fig.savefig('op1_res.png')
# fig.show()

pass
# %% Plot dermis OPs 
fig, ax = plt.subplots(1, 2, figsize=(22, 12), dpi=300)
# ax[0].plot(df_mua2['wl'], df_mua2['Bashkatov 2005 skin'], '--', linewidth=line_width, label='A. N. Bashkatov et al.', color='tab:red')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['Bashkatov 2005 skin']-2*df_mua2['Bashkatov 2005 skin_std'], df_mua2['Bashkatov 2005 skin']+2*df_mua2['Bashkatov 2005 skin_std'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[0].plot(df_mua2['wl'], df_mua2['Salomatina 2006 dermis'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['Salomatina 2006 dermis']-2*df_mua2['Salomatina 2006 dermis_std'], df_mua2['Salomatina 2006 dermis']+2*df_mua2['Salomatina 2006 dermis_std'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[0].plot(df_mua2['wl'], df_mua2['Shimojo 2020 Asian dermis'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['Shimojo 2020 Asian dermis']-2*df_mua2['Shimojo 2020 Asian dermis_std'], df_mua2['Shimojo 2020 Asian dermis']+2*df_mua2['Shimojo 2020 Asian dermis_std'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[0].plot(df_mua2['wl'], df_mua2['Simpson 1998 caucasian skin'], '--', linewidth=line_width, label='C. R. Simpson et al. (caucasian)', color='tab:gray')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['Simpson 1998 caucasian skin']-2*df_mua2['Simpson 1998 caucasian skin_std'], df_mua2['Simpson 1998 caucasian skin']+2*df_mua2['Simpson 1998 caucasian skin_std'], alpha=0.5, edgecolor='tab:gray',facecolor='tab:gray')
# ax[0].plot(df_mua2['wl'], df_mua2['Simpson 1998 negroid skin'], '--', linewidth=line_width, label='C. R. Simpson et al. (negroid)', color='tab:olive')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['Simpson 1998 negroid skin']-2*df_mua2['Simpson 1998 negroid skin_std'], df_mua2['Simpson 1998 negroid skin']+2*df_mua2['Simpson 1998 negroid skin_std'], alpha=0.5, edgecolor='tab:olive',facecolor='tab:olive')

# ax[0].plot(df_mua2['wl'], (df_mua2['D. Yudovsky_lb']+df_mua2['D. Yudovsky_ub'])/2, ':', linewidth=line_width, label='D. Yudovsky et al', color='tab:green')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['D. Yudovsky_lb'], df_mua2['D. Yudovsky_ub'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[0].plot(df_mua2['wl'], (df_mua2['D. Yudovsky, A. J. Durkin_lb']+df_mua2['D. Yudovsky, A. J. Durkin_ub'])/2, ':', linewidth=line_width, label='D. Yudovsky, A. J. Durkin', color='tab:red')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['D. Yudovsky, A. J. Durkin_lb'], df_mua2['D. Yudovsky, A. J. Durkin_ub'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[0].plot(df_mua2['wl'], (df_mua2['S.-Y. Tsui_lb']+df_mua2['S.-Y. Tsui_ub'])/2, ':', linewidth=line_width, label='S.-Y. Tsui et al.', color='tab:purple')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['S.-Y. Tsui_lb'], df_mua2['S.-Y. Tsui_ub'], alpha=0.5, edgecolor='tab:purple',facecolor='tab:purple')
# ax[0].plot(df_mua2['wl'], (df_mua2['C.-Y. Wang_lb']+df_mua2['C.-Y. Wang_ub'])/2, ':', linewidth=line_width, label='C.-Y. Wang et al.', color='tab:brown')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['C.-Y. Wang_lb'], df_mua2['C.-Y. Wang_ub'], alpha=0.5, edgecolor='tab:brown',facecolor='tab:brown')
# ax[0].plot(df_mua2['wl'], df_mua2['H. Jonasson et al. 2023 (upper dermis)'], ':', linewidth=line_width, label='H. Jonasson et al. 2023 (upper dermis)', color='tab:pink')
# # ax[0].fill_between(df_mua2['wl'], df_mua2['H. Jonasson et al. 2023 (upper dermis)_lb'], df_mua2['H. Jonasson et al. 2023 (upper dermis)_ub'], alpha=0.5, edgecolor='tab:pink',facecolor='tab:pink')
# ax[0].plot(df_mua2['wl'], df_mua2['H. Jonasson et al. 2023 (lower dermis)'], ':', linewidth=line_width, label='H. Jonasson et al. 2023 (lower dermis)', color='tab:gray')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.forearm_a'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.forearm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.forearm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.arm_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.arm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.arm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.chest_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.chest_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.chest_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.abdomen_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.abdomen_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.abdomen_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.thigh_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.thigh_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.calf_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua2['wl'], df_mua2['G. Blaney et al.calf_b'], ':', linewidth=line_width, color='tab:blue')
# # ax[0].plot(df_sub1['wl'], df_sub1['mua2'], linewidth=line_width, label='Subject HW')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[0].plot(df_sub1['wl'], df_sub1['mua2'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[0].plot(df_sub2['wl'], df_sub2['mua2'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[0].plot(df_sub3['wl'], df_sub3['mua2'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')    

ylabel_name = '$μ_{a}$ ($cm^{-1}$)'
ax[0] = set_axes(ax[0], ylabel_name, 'mua')

# ax[1].plot(df_musp2['wl'], df_musp2['Bashkatov 2005 skin'], '--', linewidth=line_width, label='A. N. Bashkatov et al.', color='tab:red')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['Bashkatov 2005 skin']-2*df_musp2['Bashkatov 2005 skin_std'], df_musp2['Bashkatov 2005 skin']+2*df_musp2['Bashkatov 2005 skin_std'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[1].plot(df_musp2['wl'], df_musp2['Salomatina 2006 dermis'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['Salomatina 2006 dermis']-2*df_musp2['Salomatina 2006 dermis_std'], df_musp2['Salomatina 2006 dermis']+2*df_musp2['Salomatina 2006 dermis_std'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[1].plot(df_musp2['wl'], df_musp2['Shimojo 2020 Asian dermis'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['Shimojo 2020 Asian dermis']-2*df_musp2['Shimojo 2020 Asian dermis_std'], df_musp2['Shimojo 2020 Asian dermis']+2*df_musp2['Shimojo 2020 Asian dermis_std'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[1].plot(df_musp2['wl'], df_musp2['Simpson 1998 caucasian skin'], '--', linewidth=line_width, label='C. R. Simpson et al. (caucasian)', color='tab:gray')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['Simpson 1998 caucasian skin']-2*df_musp2['Simpson 1998 caucasian skin_std'], df_musp2['Simpson 1998 caucasian skin']+2*df_musp2['Simpson 1998 caucasian skin_std'], alpha=0.5, edgecolor='tab:gray',facecolor='tab:gray')
# ax[1].plot(df_musp2['wl'], df_musp2['Simpson 1998 negroid skin'], '--', linewidth=line_width, label='C. R. Simpson et al. (negroid)', color='tab:olive')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['Simpson 1998 negroid skin']-2*df_musp2['Simpson 1998 negroid skin_std'], df_musp2['Simpson 1998 negroid skin']+2*df_musp2['Simpson 1998 negroid skin_std'], alpha=0.5, edgecolor='tab:olive',facecolor='tab:olive')
# ax[1].plot(df_musp2['wl'], df_musp2['H. Jonasson'], ':', linewidth=line_width, label='H. Jonasson et al. 2018', color='tab:olive')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['H. Jonasson']-2*df_musp2['H. Jonasson_std'], df_musp2['H. Jonasson']+2*df_musp2['H. Jonasson_std'], alpha=0.5, edgecolor='tab:olive',facecolor='tab:olive')
# ax[1].plot(df_musp2['wl'], df_musp2['H. Jonasson et al. 2023'], ':', linewidth=line_width, label='H. Jonasson et al. 2023', color='tab:orange')
# # ax[1].fill_between(df_musp2['wl'], df_musp2['H. Jonasson et al. 2023_lb'], df_musp2['H. Jonasson et al. 2023_ub'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (forearm_A)'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (forearm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (forearm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (arm_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (arm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (arm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (chest_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (chest_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (chest_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (abdomen_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (abdomen_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (abdomen_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (thigh_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (thigh_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (thigh_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (calf_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (calf_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp2['wl'], df_musp2['G. Blaney et al. (calf_C)'], ':', linewidth=line_width, color='tab:blue')

# ax[1].plot(df_sub1['wl'], 0.285*df_sub1['mus2'], linewidth=line_width, label='Subject HW')
if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[1].plot(df_sub1['wl'], 0.285*df_sub1['mus2'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[1].plot(df_sub2['wl'], 0.285*df_sub2['mus2'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[1].plot(df_sub3['wl'], 0.285*df_sub3['mus2'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')

ylabel_name = '$μ_{s}$\' ($cm^{-1}$)'
ax[1] = set_axes(ax[1], ylabel_name, 'mus')

fig.suptitle('Dermis', fontsize=label_size+4)
fig.savefig('op2_res.png')
# fig.show()

pass
# %% Plot subcu. OPs 
fig, ax = plt.subplots(1, 2, figsize=(22, 12), dpi=300)
# # ax[0] = brokenaxes(ylims=((0, 1.4), (2.2, 5)),despine=False, hspace=0.05,d=0.01)
# ax[0].plot(df_mua3['wl'], df_mua3['Bashkatov 2005'], '--', linewidth=line_width, label='A. N. Bashkatov et al.', color='tab:red')
# # ax[0].fill_between(df_mua3['wl'], df_mua3['Bashkatov 2005']-2*df_mua3['Bashkatov 2005_std'], df_mua3['Bashkatov 2005']+2*df_mua3['Bashkatov 2005_std'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[0].plot(df_mua3['wl'], df_mua3['Salomatina 2006'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[0].fill_between(df_mua3['wl'], df_mua3['Salomatina 2006']-2*df_mua3['Salomatina 2006_std'], df_mua3['Salomatina 2006']+2*df_mua3['Salomatina 2006_std'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[0].plot(df_mua3['wl'], df_mua3['Shimojo 2020 Asian'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[0].fill_between(df_mua3['wl'], df_mua3['Shimojo 2020 Asian']-2*df_mua3['Shimojo 2020 Asian_std'], df_mua3['Shimojo 2020 Asian']+2*df_mua3['Shimojo 2020 Asian_std'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[0].plot(df_mua3['wl'], df_mua3['Simpson 1998'], '--', linewidth=line_width, label='C. R. Simpson et al.', color='tab:blue')
# # ax[0].fill_between(df_mua3['wl'], df_mua3['Simpson 1998']-2*df_mua3['Simpson 1998_std'], df_mua3['Simpson 1998']+2*df_mua3['Simpson 1998_std'], alpha=0.5, edgecolor='tab:blue',facecolor='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['H. Jonasson et al. 2023 (lower dermis)'], ':', linewidth=line_width, label='H. Jonasson et al. 2023 (lower dermis)', color='tab:gray')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.forearm_a'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.forearm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.forearm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.arm_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.arm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.arm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.chest_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.chest_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.chest_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.abdomen_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.abdomen_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.abdomen_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.thigh_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.thigh_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.calf_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua3['wl'], df_mua3['G. Blaney et al.calf_b'], ':', linewidth=line_width, color='tab:blue')
# # ax[0].plot(df_sub1['wl'], df_sub1['mua3'], linewidth=line_width, label='Subject HW')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[0].plot(df_sub1['wl'], df_sub1['mua3'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[0].plot(df_sub2['wl'], df_sub2['mua3'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[0].plot(df_sub3['wl'], df_sub3['mua3'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')      

ylabel_name = '$μ_{a}$ ($cm^{-1}$)'
ax[0] = set_axes(ax[0], ylabel_name, 'mua')

# ax[1].plot(df_musp3['wl'], df_musp3['Bashkatov 2005'], '--', linewidth=line_width, label='A. N. Bashkatov et al.', color='tab:red')
# # ax[1].fill_between(df_musp3['wl'], df_musp3['Bashkatov 2005']-2*df_musp3['Bashkatov 2005_std'], df_musp3['Bashkatov 2005']+2*df_musp3['Bashkatov 2005_std'], alpha=0.5, edgecolor='tab:red',facecolor='tab:red')
# ax[1].plot(df_musp3['wl'], df_musp3['Salomatina 2006'], '--', linewidth=line_width, label='E. Salomatina et al.', color='tab:orange')
# # ax[1].fill_between(df_musp3['wl'], df_musp3['Salomatina 2006']-2*df_musp3['Salomatina 2006_std'], df_musp3['Salomatina 2006']+2*df_musp3['Salomatina 2006_std'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[1].plot(df_musp3['wl'], df_musp3['Shimojo 2020 Asian'], '--', linewidth=line_width, label='Y. Shimojo et al.', color='tab:green')
# # ax[1].fill_between(df_musp3['wl'], df_musp3['Shimojo 2020 Asian']-2*df_musp3['Shimojo 2020 Asian_std'], df_musp3['Shimojo 2020 Asian']+2*df_musp3['Shimojo 2020 Asian_std'], alpha=0.5, edgecolor='tab:green',facecolor='tab:green')
# ax[1].plot(df_musp3['wl'], df_musp3['Simpson 1998'], '--', linewidth=line_width, label='C. R. Simpson et al.', color='tab:blue')
# # ax[1].fill_between(df_musp3['wl'], df_musp3['Simpson 1998']-2*df_musp3['Simpson 1998_std'], df_musp3['Simpson 1998']+2*df_musp3['Simpson 1998_std'], alpha=0.5, edgecolor='tab:blue',facecolor='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['H. Jonasson et al. 2023'], ':', linewidth=line_width, label='H. Jonasson et al. 2023', color='tab:orange')
# # ax[1].fill_between(df_musp3['wl'], df_musp3['H. Jonasson et al. 2023_lb'], df_musp3['H. Jonasson et al. 2023_ub'], alpha=0.5, edgecolor='tab:orange',facecolor='tab:orange')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (forearm_A)'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (forearm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (forearm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (arm_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (arm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (arm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (chest_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (chest_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (chest_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (abdomen_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (abdomen_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (abdomen_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (thigh_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (thigh_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (thigh_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (calf_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (calf_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp3['wl'], df_musp3['G. Blaney et al. (calf_C)'], ':', linewidth=line_width, color='tab:blue')

# # ax[1].plot(df_sub1['wl'], 0.1*df_sub1['mus3'], linewidth=line_width, label='Subject HW')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[1].plot(df_sub1['wl'], 0.1*df_sub1['mus3'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[1].plot(df_sub2['wl'], 0.1*df_sub2['mus3'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[1].plot(df_sub3['wl'], 0.1*df_sub3['mus3'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')    


ylabel_name = '$μ_{s}$\' ($cm^{-1}$)'
ax[1] = set_axes(ax[1], ylabel_name, 'mus')


fig.suptitle('Subcutaneous adipose', fontsize=label_size+4)
fig.savefig('op3_res.png')
# fig.show()

pass
# %% Plot muscle. OPs 
fig, ax = plt.subplots(1, 2, figsize=(22, 12), dpi=300)
# ax[0].plot(df_mua4['wl'], df_mua4['(Rat)Nilsson 1995'], '--', linewidth=line_width, label='A. M. K. Nilsson et al.', color='tab:purple')
# ax[0].plot(df_mua4['wl'], df_mua4['Simpson 1998'], '--', linewidth=line_width, label='C. R. Simpson et al.', color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['(Beef)Xia, Jinjun 2006'], '--', linewidth=line_width, label='J. Xia et al.', color='tab:brown')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.forearm_a'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.forearm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.forearm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.arm_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.arm_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.arm_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.chest_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.chest_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.chest_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.abdomen_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.abdomen_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.abdomen_c'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.thigh_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.thigh_b'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.calf_a'], ':', linewidth=line_width, color='tab:blue')
# ax[0].plot(df_mua4['wl'], df_mua4['G. Blaney et al.calf_b'], ':', linewidth=line_width, color='tab:blue')

# # ax[0].plot(df_sub1['wl'], df_sub1['mua4'], linewidth=line_width, label='Subject HW')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[0].plot(df_sub1['wl'], df_sub1['mua4'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[0].plot(df_sub2['wl'], df_sub2['mua4'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[0].plot(df_sub3['wl'], df_sub3['mua4'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')      


ylabel_name = '$μ_{a}$ ($cm^{-1}$)'
ax[0] = set_axes(ax[0], ylabel_name, 'mua')

# ax[1].plot(df_musp4['wl'], df_musp4['(Rat)Nilsson 1995'], '--', linewidth=line_width, label='A. M. K. Nilsson et al.', color='tab:purple')
# ax[1].plot(df_musp4['wl'], df_musp4['Simpson 1998'], '--', linewidth=line_width, label='C. R. Simpson et al.', color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['(Beef)Xia, Jinjun 2006'], '--', linewidth=line_width, label='J. Xia et al.', color='tab:brown')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (forearm_A)'], ':', linewidth=line_width, label='G. Blaney et al.', color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (forearm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (forearm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (arm_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (arm_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (arm_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (chest_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (chest_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (chest_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (abdomen_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (abdomen_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (abdomen_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (thigh_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (thigh_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (thigh_C)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (calf_A)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (calf_B)'], ':', linewidth=line_width, color='tab:blue')
# ax[1].plot(df_musp4['wl'], df_musp4['G. Blaney et al. (calf_C)'], ':', linewidth=line_width, color='tab:blue')
# # ax[1].plot(df_sub1['wl'], 0.07*df_sub1['mus4'], linewidth=line_width, label='Subject HW')

if plotSub1:
    for i in sub1plot_index:
        df_sub1 = sub1_list[i-1]
        ax[1].plot(df_sub1['wl'], 0.1*df_sub1['mus4'], linewidth=line_width, label=f'Subject 1_{i}', marker=marker[i-1], color='tab:blue')
if plotSub2:
    for i in sub2plot_index:
        df_sub2 = sub2_list[i-1]
        ax[1].plot(df_sub2['wl'], 0.1*df_sub2['mus4'], linewidth=line_width, label=f'Subject 2_{i}', marker=marker[i-1], color='tab:green')
if plotSub3:
    for i in sub3plot_index:
        df_sub3 = sub3_list[i-1]
        ax[1].plot(df_sub3['wl'], 0.1*df_sub3['mus4'], linewidth=line_width, label=f'Subject 3_{i}', marker=marker[i-1], color='tab:red')   
    
ylabel_name = '$μ_{s}$\' ($cm^{-1}$)'
ax[1] = set_axes(ax[1], ylabel_name, 'mus')

fig.suptitle('Muscle', fontsize=label_size+4)
fig.savefig('op4_res.png')
# fig.show()

pass