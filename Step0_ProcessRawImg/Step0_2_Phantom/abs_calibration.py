"""
This script do absoluted intensity calibration
Input: simulated spectra, measured spectra
Output: figure of simulated spectra & measured spectra
"""

# %%
import os 
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.colors as mcolors
import itertools
from math import comb
from tqdm import tqdm
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression


def let_one_out(x, y):
    #  -> list(LinearRegression,...)
    """let 1 of x and y out, return LinearRegression

    Args:
        x (array_like): _description_
        y (array_like): _description_
    """
    nx, mx = x.shape[0], x.shape[1]
    ny = y.shape[0]
    tx = np.ones((nx, mx), dtype=np.bool_)
    ty = np.ones(ny, dtype=np.bool_)
    reg = []
    
    # All phantoms
    r = LinearRegression().fit(x, y)
    reg.append(r)
    
    # Let 1 out
    for row in range(len(x)):
        dtx = tx.copy()
        dty = ty.copy()
        dtx[-row-1, 0] = False
        dty[-row-1] = False
        r = LinearRegression().fit(x[dtx, np.newaxis], y[dty])
        reg.append(r)
    return reg

def comb_num(num, c):
    if c == num-1:
        return comb(num, num-1)
    else:
        return comb(num, c) + comb_num(num, c-1)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

# %% Default
# PNAME = 'CHIK'
# PNAME = ['2', '3', '4', '5', '6']
PNAME = ['3', '4', '5','6']
# PNAME = ['22', '33', '44', '55', '66']
# PNAME = ['33', '44', '55', '66']
# PNAME = ['33', '44', '55', '66']
# PNAME = ['22', '33', '44', '55', '66']
# PNAME = ['CC', 'HH', 'II', 'KK']
# PNAME = ['22', '33', '44', '55', '66', 'CC', 'HH', 'II', 'KK']
# PNAME = ['2', '3', '4', '5', '6', '22', '33', '44', '55', '66']
# PNAME = ['C', 'H', 'I', 'K', 'CC', 'HH', 'II', 'KK']
SDS_LIST = [4.5, 7.5, 10.5]

# simpath = 's_out_1e9_reflectance_3456_new'
simpath = 'fromExp2'
measpath = 'm_out_20231026_kb'
oname = 'sr_'.join(PNAME) + '_' + measpath + '_' + simpath
simpath = os.path.join('PhantomSim', simpath)
measpath = os.path.join('MeasureData', measpath)
ofolder = os.path.join('AbsCalibration', oname)

if not os.path.exists(ofolder):
    os.makedirs(ofolder)

# SP_WL = np.array([700, 708, 716, 724, 732, 739, 745, 752, 759, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
# SP_WL = np.array([700,702,704,706,708,710,712,714,716,718,720,722,724,726,728,730,732,734,736,738,740,742,744,746,748,750,752,754,756,758,760,762,764,766,768,770,772,774,776,778,780,782,784,786,788,790,792,794,796,798,800,802,804,806,808,810,812,814,816,818,820,822,824,826,828,830,832,834,836,838,840,842,844,846,848,850,852,854,856,858,860,862,864,866,868,870,872,874,876,878,880])
SP_WL = np.arange(700,901)
# SP_WL = np.array([698.916,699.5632,700.2104,700.8576,701.5048,702.152,702.7992,703.4464,704.0936,704.7408,705.388,706.0352,706.6824,707.3296,707.9768,708.624,709.2712,709.9184,710.5656,711.2128,711.86,712.5072,713.1544,713.8016,714.4488,715.096,715.7432,716.3904,717.0376,717.6848,718.332,718.9792,719.6264,720.2736,720.9208,721.568,722.2152,722.8624,723.5096,724.1568,724.804,725.4512,726.0984,726.7456,727.3928,728.04,728.6872,729.3344,729.9816,730.6288,731.276,731.9232,732.5704,733.2176,733.8648,734.512,735.1592,735.8064,736.4536,737.1008,737.748,738.3952,739.0424,739.6896,740.3368,740.984,741.6312,742.2784,742.9256,743.5728,744.22,744.8672,745.5144,746.1616,746.8088,747.456,748.1032,748.7504,749.3976,750.0448,750.692,751.3392,751.9864,752.6336,753.2808,753.928,754.5752,755.2224,755.8696,756.5168,757.164,757.8112,758.4584,759.1056,759.7528,760.4,761.0472,761.6944,762.3416,762.9888,763.636,764.2832,764.9304,765.5776,766.2248,766.872,767.5192,768.1664,768.8136,769.4608,770.108,770.7552,771.4024,772.0496,772.6968,773.344,773.9912,774.6384,775.2856,775.9328,776.58,777.2272,777.8744,778.5216,779.1688,779.816,780.4632,781.1104,781.7576,782.4048,783.052,783.6992,784.3464,784.9936,785.6408,786.288,786.9352,787.5824,788.2296,788.8768,789.524,790.1712,790.8184,791.4656,792.1128,792.76,793.4072,794.0544,794.7016,795.3488,795.996,796.6432,797.2904,797.9376,798.5848,799.232,799.8792,800.5264,801.1736,801.8208,802.468,803.1152,803.7624,804.4096,805.0568,805.704,806.3512,806.9984,807.6456,808.2928,808.94,809.5872,810.2344,810.8816,811.5288,812.176,812.8232,813.4704,814.1176,814.7648,815.412,816.0592,816.7064,817.3536,818.0008,818.648,819.2952,819.9424,820.5896,821.2368,821.884,822.5312,823.1784,823.8256,824.4728,825.12,825.7672,826.4144,827.0616,827.7088,828.356,829.0032,829.6504,830.2976,830.9448,831.592,832.2392,832.8864,833.5336,834.1808,834.828,835.4752,836.1224,836.7696,837.4168,838.064,838.7112,839.3584,840.0056,840.6528,841.3,841.9472,842.5944,843.2416,843.8888,844.536,845.1832,845.8304,846.4776,847.1248,847.772,848.4192,849.0664,849.7136,850.3608,851.008,851.6552,852.3024,852.9496,853.5968,854.244,854.8912,855.5384,856.1856,856.8328,857.48,858.1272,858.7744,859.4216,860.0688,860.716,861.3632,862.0104,862.6576,863.3048,863.952,864.5992,865.2464,865.8936,866.5408,867.188,867.8352,868.4824,869.1296,869.7768,870.424,871.0712,871.7184,872.3656,873.0128,873.66,874.3072,874.9544,875.6016,876.2488,876.896,877.5432,878.1904,878.8376,879.4848,880.132,880.7792,881.4264,882.0736])
# SP_WL = np.array([699.8298, 706.2727, 712.7156,	719.1585, 725.6014,	732.0443,
#                 738.4872, 744.9301, 751.373, 757.8159, 764.2588, 770.7017, 
#                 777.1446, 783.5875, 790.0304, 796.4733, 802.9162, 809.3591,
#                 815.802, 822.2449, 828.6878, 835.1307, 841.5736, 848.0165, 
#                 854.4594, 860.9023, 867.3452, 873.7881, 880.231])

# %% Process sim & meas spectra
# Process measured spectra
det_list = []
sim_list = []
for pid in PNAME:
    df = pd.read_csv(os.path.join(measpath, f'{pid}_det_mean.csv'))
    # SP_WL = df['wl']
    d1 = {'wl':SP_WL}
    d2 = {f'ch{i+1}':np.interp(SP_WL, df['wl'], df[f'ch{i+1}_mean']) for i in range(3)}
    d = {**d1, **d2}
    dfs = pd.DataFrame(data=d)
    det_list.append(dfs)
    
# Process simulated spectra
for pid in PNAME:    
    # df = pd.read_csv(os.path.join(simpath, f'reflectance_{pid}.csv'))
    df = pd.read_csv(os.path.join(simpath, f'reflectance_{pid}.csv'))
    d1 = {'wl':SP_WL}
    # t = moving_average(df[f'ch1'], 5)
    d2 = {f'ch1':np.interp(SP_WL, df['wl'], df[f'ch1'])}
    d3 = {f'ch2':np.interp(SP_WL, df['wl'], df[f'ch2'])}
    d4 = {f'ch3':np.interp(SP_WL, df['wl'], df[f'ch3'])}
    d = {**d1, **d2, **d3, **d4}
    dfs = pd.DataFrame(data=d)
    sim_list.append(dfs)
    # plt.figure()
    # plt.plot(d1['wl'], d2['ch2'])
    # plt.plot(d1['wl'], df['ch2'].iloc[10:-10])
    
    # plt.show()
    # pass
d_ch1 = {'wl':SP_WL}
d_ch2 = {'wl':SP_WL}
d_ch3 = {'wl':SP_WL}
for i, pid in enumerate(PNAME):
    temp_d1 = {f'sim_{PNAME[i]}': sim_list[i]['ch1'].values,
               f'meas_{PNAME[i]}': det_list[i]['ch1'].values,}
    temp_d2 = {f'sim_{PNAME[i]}': sim_list[i]['ch2'].values,
               f'meas_{PNAME[i]}': det_list[i]['ch2'].values,}
    temp_d3 = {f'sim_{PNAME[i]}': sim_list[i]['ch3'].values,
               f'meas_{PNAME[i]}': det_list[i]['ch3'].values,}
    d_ch1 = {**d_ch1, **temp_d1}
    d_ch2 = {**d_ch2, **temp_d2}
    d_ch3 = {**d_ch3, **temp_d3}
df_ch1 = pd.DataFrame(data=d_ch1)
df_ch2 = pd.DataFrame(data=d_ch2)
df_ch3 = pd.DataFrame(data=d_ch3)
df_ch1.to_csv(os.path.join(ofolder, 'ch1.csv'), index=False)
df_ch2.to_csv(os.path.join(ofolder, 'ch2.csv'), index=False)
df_ch3.to_csv(os.path.join(ofolder, 'ch3.csv'), index=False)

# %% Plot phantom
# PNAME = '3'
fig1, ax1 = plt.subplots(1, SP_WL.size, figsize=(20, 25), dpi=300)
fig2, ax2 = plt.subplots(1, SP_WL.size, figsize=(20, 25), dpi=300)
fig3, ax3 = plt.subplots(1, SP_WL.size, figsize=(20, 25), dpi=300)
# fig1, ax1 = plt.subplots(1, 3, figsize=(12, 6))
# fig2, ax2 = plt.subplots(1, 1, dpi=300)
# fig3, ax3 = plt.subplots(1, 1, dpi=300)
r2_arr = np.zeros((comb_num(len(PNAME), len(PNAME)), 3))

reg_list11 = [] # wl[combination[]]
reg_list22 = [] 
reg_list33 = [] 
for i, wl in tqdm(enumerate(SP_WL)):
    for pid in PNAME:
        ax1[i].scatter(df_ch1.loc[i, f'meas_{pid}'], df_ch1.loc[i, f'sim_{pid}'], label=f'Phantom {pid}')
        ax2[i].scatter(df_ch2.loc[i, f'meas_{pid}'], df_ch2.loc[i, f'sim_{pid}'], label=f'Phantom {pid}')
        ax3[i].scatter(df_ch3.loc[i, f'meas_{pid}'], df_ch3.loc[i, f'sim_{pid}'], label=f'Phantom {pid}')
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    # if wl == 800:
    #     for j, pid in enumerate(PNAME):
    #         ax1[0].scatter(df_ch1.loc[i, f'meas_{pid}'], df_ch1.loc[i, f'sim_{pid}'], label=f'Phantom {pid}', marker='o', c='none', edgecolors=colors[j], s=60)
    #         ax1[1].scatter(df_ch2.loc[i, f'meas_{pid}'], df_ch2.loc[i, f'sim_{pid}'], label=f'Phantom {pid}', marker='o', c='none', edgecolors=colors[j], s=60)
    #         ax1[2].scatter(df_ch3.loc[i, f'meas_{pid}'], df_ch3.loc[i, f'sim_{pid}'], label=f'Phantom {pid}', marker='o', c='none', edgecolors=colors[j], s=60)
    meas_cols = [2 * (k+1) for k in range(len(PNAME))]
    sim_cols = [2*k + 1 for k in range(len(PNAME))]
    x1, y1 = df_ch1.iloc[i, meas_cols].values, df_ch1.iloc[i, sim_cols].values
    x2, y2 = df_ch2.iloc[i, meas_cols].values, df_ch2.iloc[i, sim_cols].values
    x3, y3 = df_ch3.iloc[i, meas_cols].values, df_ch3.iloc[i, sim_cols].values
    x1 = x1[:, np.newaxis]
    x2 = x2[:, np.newaxis]
    x3 = x3[:, np.newaxis]
    
    # Let a phantom out
    reg_list1 = let_one_out(x1, y1)
    reg_list2 = let_one_out(x2, y2)
    reg_list3 = let_one_out(x3, y3)
    reg_list11.append(reg_list1)
    reg_list22.append(reg_list2)
    reg_list33.append(reg_list3)
    for com in range(len(reg_list1)):
        r2_arr[com, 0] += reg_list1[com].score(x1, y1)
        r2_arr[com, 1] += reg_list2[com].score(x2, y2)
        r2_arr[com, 2] += reg_list3[com].score(x3, y3)
    reg_ch1 = LinearRegression().fit(x1, y1)
    reg_ch2 = LinearRegression().fit(x2, y2)
    reg_ch3 = LinearRegression().fit(x3, y3)
    r2_ch1 = r2_score(y1, reg_ch1.predict(x1))
    r2_ch2 = r2_score(y2, reg_ch2.predict(x2))
    r2_ch3 = r2_score(y3, reg_ch3.predict(x3))
    
    ax1[i].plot(x1, reg_ch1.predict(x1), linestyle='--')
    ax2[i].plot(x2, reg_ch2.predict(x2), linestyle='--')
    ax3[i].plot(x3, reg_ch3.predict(x3), linestyle='--')
    ax1[i].text(0.85, 0.9, f'R$^2$ = {r2_ch1:>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    ax2[i].text(0.85, 0.9, f'R$^2$ = {r2_ch2:>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    ax3[i].text(0.85, 0.9, f'R$^2$ = {r2_ch3:>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    # ax1[i].text(0.1, 0.9, f'R$^2$ = {reg_ch1.score(x1, y1):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    # ax2[i].text(0.1, 0.9, f'R$^2$ = {reg_ch2.score(x2, y2):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    # ax3[i].text(0.1, 0.9, f'R$^2$ = {reg_ch3.score(x3, y3):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1[i].transAxes)
    ax1[i].set_xlabel('Gray values (counts)')
    ax1[i].set_ylabel('Reflectance (-)')
    # ax1[i].set_xticks(np.array([0, 17500, 35000, 52500, 70000]))
    # ax1[i].set_xticks(np.linspace(0, 20000, 5))
    # ax1[i].set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    ax1[i].set_title(f'{wl} nm')
    ax1[i].grid(visible=True)
    ax2[i].set_xlabel('Gray values (counts)')
    ax2[i].set_ylabel('Reflectance (-)')
    # ax2[i].set_xticks(np.array([0, 22500, 45000, 67500, 90000]))
    # ax2[i].set_xticks(np.linspace(0, 40000, 5))
    # ax2[i].set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    ax2[i].set_title(f'{wl} nm')
    ax2[i].grid(visible=True)
    ax3[i].set_xlabel('Gray values (counts)')
    ax3[i].set_ylabel('Reflectance (-)')
    # ax3[i].set_xticks(np.array([0, 22500, 45000, 67500, 90000]))
    # ax3[i].set_xticks(np.linspace(0, 90000, 5))
    # ax3[i].set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    ax3[i].set_title(f'{wl} nm')
    ax3[i].grid(visible=True)
    # if wl == 800:
    #     font = 16
    #     ax1[0].plot(x1, reg_ch1.predict(x1), linestyle='--')
    #     ax1[1].plot(x2, reg_ch2.predict(x2), linestyle='--')
    #     ax1[2].plot(x3, reg_ch3.predict(x3), linestyle='--')
    #     ax1[0].text(16000, 2.1e-8, f'R$^2$ = {r2_ch2:>.2f}', horizontalalignment='center', verticalalignment='center', fontsize=font)
    #     ax1[1].text(33000, 1.6e-8, f'R$^2$ = {r2_ch2:>.2f}', horizontalalignment='center', verticalalignment='center', fontsize=font)
    #     ax1[2].text(80000, 1.4e-8, f'R$^2$ = {r2_ch3:>.2f}', horizontalalignment='center', verticalalignment='center', fontsize=font)
    #     # ax1.text(0.1, 0.9, f'R$^2$ = {reg_ch1.score(x1, y1):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    #     # ax2.text(0.1, 0.9, f'R$^2$ = {reg_ch2.score(x2, y2):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    #     # ax3.text(0.1, 0.9, f'R$^2$ = {reg_ch3.score(x3, y3):>.4f}', horizontalalignment='center', verticalalignment='center', transform=ax1.transAxes)
    #     # ax1[0].set_xlabel('Gray values (counts)', fontsize=font)
    #     ax1[0].set_ylabel('Reflectance', fontsize=font)
    #     # ax1.set_xticks(np.array([0, 17500, 35000, 52500, 70000]))
    #     # ax1.set_xticks(np.linspace(0, 20000, 5))
    #     # ax1.set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    #     ax1[0].set_title(f'SDS = 4.5 mm', fontsize=font)
    #     ax1[0].grid(visible=True, linestyle='--')
    #     ax1[1].set_xlabel('Photon counts', fontsize=font)
    #     # ax1[1].set_ylabel('Reflectance', fontsize=font)
    #     # ax2.set_xticks(np.array([0, 22500, 45000, 67500, 90000]))
    #     # ax2.set_xticks(np.linspace(0, 40000, 5))
    #     # ax2.set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    #     ax1[1].set_title(f'SDS = 7.5 mm', fontsize=font)
    #     ax1[1].grid(visible=True, linestyle='--')
    #     # ax1[2].set_xlabel('Gray values (counts)', fontsize=font)
    #     # ax1[2].set_ylabel('Reflectance', fontsize=font)
    #     # ax3.set_xticks(np.array([0, 22500, 45000, 67500, 90000]))
    #     # ax3.set_xticks(np.linspace(0, 90000, 5))
    #     # ax3.set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
    #     ax1[2].set_title(f'SDS = 10.5 mm', fontsize=font)
    #     ax1[2].grid(visible=True, linestyle='--')
    #     ax1[0].tick_params(axis='both', which='major', labelsize=font-4)
    #     ax1[1].tick_params(axis='both', which='major', labelsize=font-4)
    #     ax1[2].tick_params(axis='both', which='major', labelsize=font-4)
    #     ax1[2].legend(loc='lower right', bbox_to_anchor=(1, 0.2), frameon=False, fontsize=font-4)
    # if i == 4:
    #     ax1[i].legend(loc='upper right', bbox_to_anchor=(1.5, 1.))
    #     ax2[i].legend(loc='upper right', bbox_to_anchor=(1.5, 1.))
    #     ax3[i].legend(loc='upper right', bbox_to_anchor=(1.5, 1.))

gs1 = matplotlib.gridspec.GridSpec(20, 11, figure=fig1)
gs2 = matplotlib.gridspec.GridSpec(20, 11, figure=fig1)
gs3 = matplotlib.gridspec.GridSpec(20, 11, figure=fig1)
for i, ax in enumerate(fig1.axes):
    ax1[i].set_position(gs1[i].get_position(fig1))
    ax2[i].set_position(gs2[i].get_position(fig2))
    ax3[i].set_position(gs3[i].get_position(fig3))
fig1.suptitle(f'SDS = {SDS_LIST[0]} mm', y=0.93, fontsize=20)
fig2.suptitle(f'SDS = {SDS_LIST[1]} mm', y=0.93, fontsize=20)
fig3.suptitle(f'SDS = {SDS_LIST[2]} mm', y=0.93, fontsize=20)
fig1.tight_layout()
fig2.tight_layout()
fig3.tight_layout()
fig1.savefig(os.path.join(ofolder, 'ch1.png'))
fig2.savefig(os.path.join(ofolder, 'ch2.png'))
fig3.savefig(os.path.join(ofolder, 'ch3.png'))

# %% Process r2_arr
r2_arr /= SP_WL.size
index = [','.join(PNAME)] + [','.join(x) for x in itertools.combinations(PNAME, len(PNAME)-1)]
column = [f'SDS = {SDS_LIST[i]} mm' for i in range(3)]
df_r2 = pd.DataFrame(data=r2_arr, columns=column, index=index)
df_r2.to_csv(os.path.join(ofolder, 'r2_score.csv'))

# %% Process regression coefficient
# Choose all
coef_arr = np.zeros((SP_WL.size, 2*3 + 1))
coef_arr[:, 0] = SP_WL
for i, wl in tqdm(enumerate(SP_WL)):
    reg1 = reg_list11[i][0]
    reg2 = reg_list22[i][0]
    reg3 = reg_list33[i][0]
    coef_arr[i, 1] = reg1.coef_
    coef_arr[i, 2] = reg1.intercept_
    coef_arr[i, 3] = reg2.coef_
    coef_arr[i, 4] = reg2.intercept_
    coef_arr[i, 5] = reg3.coef_
    coef_arr[i, 6] = reg3.intercept_
col = ['wl', '1a', '1b', '2a', '2b', '3a', '3b']
df_reg = pd.DataFrame(coef_arr, columns=col)
df_reg.to_csv(os.path.join(ofolder, 'reg.csv'), index=False)

# %% Choose best result to calibrate
p_list = PNAME.copy()
reg_list = list(range(len(p_list), 0, -1))
# p_list = ['22', '33', '44', '55', '66']
# p_list = [ '3', '4', '5', '6']
# reg_list = [4, 3, 2, 1]
# p_choose = '22'
# reg_choose = 5
d_rms = {'target': p_list,
         'ch1': np.zeros(len(p_list)),
         'ch2': np.zeros(len(p_list)),
         'ch3': np.zeros(len(p_list))}
df_rms = pd.DataFrame(data=d_rms)

font=16
for pid, (p_choose, reg_choose) in enumerate(zip(p_list, reg_list)):
    ms1 = np.zeros(SP_WL.shape)
    ms2 = np.zeros(SP_WL.shape)
    ms3 = np.zeros(SP_WL.shape)
    for i, wl in tqdm(enumerate(SP_WL)):
        ms1[i] = df_ch1.loc[i, f'meas_{p_choose}']
        ms2[i] = df_ch2.loc[i, f'meas_{p_choose}']
        ms3[i] = df_ch3.loc[i, f'meas_{p_choose}']
        ms1[i] = reg_list11[i][reg_choose].predict(ms1[i, np.newaxis, np.newaxis])
        ms2[i] = reg_list22[i][reg_choose].predict(ms2[i, np.newaxis, np.newaxis])
        ms3[i] = reg_list33[i][reg_choose].predict(ms3[i, np.newaxis, np.newaxis])
        
    # Plot calibrated and simulated result
    fig, ax = plt.subplots(1, 3, figsize=(12, 6), dpi=300)
    ax[0].plot(SP_WL, ms1, 'r--',
            SP_WL, df_ch1[f'sim_{p_choose}'], 'b-')
    ax[1].plot(SP_WL, ms2, 'r--',
            SP_WL, df_ch2[f'sim_{p_choose}'], 'b-')
    ax[2].plot(SP_WL, ms3, 'r--',
            SP_WL, df_ch3[f'sim_{p_choose}'], 'b-')
    y_pred = [ms1, ms2, ms3]
    y_true = [df_ch1[f'sim_{p_choose}'].values, df_ch2[f'sim_{p_choose}'].values, df_ch3[f'sim_{p_choose}'].values]

    for i in range(3):
        rmspe = np.sum(((y_pred[i]-y_true[i])/y_true[i])**2) / y_true[i].size
        rmspe = np.sqrt(rmspe) 
        df_rms.iloc[pid, i+1] = rmspe
        rmspe *= 100 
        if i == 1:
            ax[i].set_xlabel('Wavelength (nm)', fontsize=font)
        elif i == 0:
            ax[i].set_ylabel('Reflectance', fontsize=font)
        ax[i].set_title(f'SDS = {SDS_LIST[i]} mm', fontsize=font)
        ax[i].text(0.7, 0.8, f'RMSPE = {rmspe:>.1f} %', horizontalalignment='center', verticalalignment='center', transform=ax[i].transAxes, fontsize=font-4)
        ax[i].set_xticks(np.arange(700, 881, 40))
        ax[i].set_yticks(np.array([0, 0.5, 1., 1.5, 2., 2.5,  3., 3.5]) * 1e-8)
        ax[i].grid(visible=True, linestyle='--')
        ax[i].tick_params(axis='both', which='major', labelsize=font-4)
    fig.legend(labels=['Fitted', 'Simulated'], loc='upper right', bbox_to_anchor=(0.9, 0.85), frameon=False, fontsize=font-4)
    fig.suptitle(f'Phantom {p_choose}', fontsize=font)
    fig.tight_layout()
    fig.savefig(os.path.join(ofolder, f'calibrated_{p_choose}.png'))
df_rms.to_csv(os.path.join(ofolder, 'rmspe.csv'), index=False)
print('Finished !')
# %%
