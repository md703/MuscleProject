import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
from glob import glob
from natsort import natsorted
from tqdm import tqdm

def moving_average(x, w):
    for i in range(3):
        x.iloc[1:-1, i] = np.convolve(x.iloc[:, i].values, np.ones(w), 'valid')
        x.iloc[1:-1, i] /= w
    return x
    # return np.convolve(x, np.ones(w), 'valid') / w

subject = 'eu'
path = 'eu_test'
font = 30
folder_list = glob(os.path.join(path, '*'))
folder_list = natsorted(folder_list)
# fit_wl = np.array([700, 708, 716, 724, 732, 739, 745, 752, 759, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
# fit_wl = np.array([700, 708, 716, 724, 732, 739, 742, 745, 752, 755, 757, 759, 761, 763, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
# fit_wl = np.array([700, 708, 716, 724, 732, 739, 742, 745, 748, 752, 755, 759, 763, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
fit_wl =  np.array([711,716,724,732,755,759,763,769,779,788,798,805,812,820,826,832,840,854,866,880])
# tar_wl = np.array([699.8298, 706.2727, 712.7156,	719.1585, 725.6014,	732.0443,
#                 738.4872, 744.9301, 751.373, 757.8159, 764.2588, 770.7017, 
#                 777.1446, 783.5875, 790.0304, 796.4733, 802.9162, 809.3591,
#                 815.802, 822.2449, 828.6878, 835.1307, 841.5736, 848.0165, 
#                 854.4594, 860.9023, 867.3452, 873.7881, 880.231])
# tar_wl = fit_wl
tar_wl = np.arange(680, 901)
tar_wl = np.arange(700,901)
for folder in tqdm(folder_list):
    fig, ax = plt.subplots(1, 3, figsize=(12, 8))
    figpath = os.path.join(folder, 'spec_pics_re')
    if not os.path.exists(figpath):
        os.mkdir(figpath)
        
    for nfit in range(1, 21):
        
        tarpath = os.path.join(folder, f'fit_all{nfit}', 'lsqSpec_target.txt')
        fitpath = os.path.join(folder, f'fit_all{nfit}', 'lsqSpec_final.txt')
        # mcpath = os.path.join(folder, f'fit_all{nfit}', 'final_MC_output.txt')
        parapath = os.path.join(folder, f'fit_all{nfit}', 'lsqPara_final.csv')
        
        df_tar = pd.read_csv(tarpath, sep=' ', header=None)
        df_fit = pd.read_csv(fitpath, sep=' ', header=None)
        # df_mc = pd.read_csv(mcpath, sep=' ', header=None)
        df_tar = df_tar.dropna(axis=1)
        df_fit = df_fit.dropna(axis=1)
        # df_mc = df_mc.dropna(axis=1)
        df_tar.columns = ['ch1', 'ch2', 'ch3']
        df_fit.columns = ['ch1', 'ch2', 'ch3']
        # df_mc.columns = ['ch1', 'ch2', 'ch3']
        df_para = pd.read_csv(parapath)
        SDS_LIST = [4.5, 7.5, 10.5]
        
        # df_tar = moving_average(df_tar, 3)
        df_tar['wl'] = tar_wl
        
        df_fit['wl'] = fit_wl
        # df_mc['wl'] = fit_wl
        # df_tar = df_tar.loc[20:200]
        xs = np.arange(700, 881)
        
    
        for i in range(3):
            ftar = interpolate.interp1d(df_tar['wl'], df_tar[f'ch{i+1}'], kind='cubic') 
            ffit = interpolate.interp1d(df_fit['wl'], df_fit[f'ch{i+1}'], kind='cubic') 
            # fmc = interpolate.interp1d(df_mc['wl'], df_mc[f'ch{i+1}'], kind='cubic') 
            # ytar = ftar(xs)
            # yfit = ffit(xs)
            y_true = ftar(fit_wl)
            y_pred = ffit(fit_wl)
            # y_mc = fmc(fit_wl)
            rms_fit = np.sum(((y_pred-y_true)/y_true)**2) / y_true.size
            rms_fit = 100 * np.sqrt(rms_fit) 
            # rms_mc = np.sum(((y_mc-y_true)/y_true)**2) / y_true.size
            # rms_mc = 100 * np.sqrt(rms_mc) 
            
            ax[i].set_title(f'SDS = {SDS_LIST[i]} mm', fontsize=font-8)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
            # ax[i].text(0.8, 0.8, f'RMSPE = {rmspe:>.1f} %', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=ax[i].transAxes, bbox=props)
            # ax[i].plot(xs, ytar, 'b', label='Target', linewidth=2)
            # ax[i].plot(xs, yfit, 'r--', label='Fitted', linewidth=2)
            # ax[i].plot(df_tar['wl'], df_tar[f'ch{i+1}'], 'b', label='Target', linewidth=2)
            if nfit == 1:
                # ax[i].plot(df_tar['wl'], df_tar[f'ch{i+1}'], 'b', label='Target', linewidth=2)
                ax[i].plot(fit_wl, np.interp(fit_wl, df_tar['wl'], df_tar[f'ch{i+1}']), 'b', label='Target', linewidth=2)
            ax[i].plot(df_fit['wl'], df_fit[f'ch{i+1}'], '--', label=f'Fitted {nfit}, err = {rms_fit:.2f}%', linewidth=0.7, alpha=0.5)
            # ax[i].plot(df_mc['wl'], df_mc[f'ch{i+1}'], 'g--', label=f'Fitted by MC, err = {rms_mc:.2f}%', linewidth=2)                

            if i == 2 and nfit==20:
                ax[i].set_ylabel('Reflectance', fontsize=font-4)
                ax[i].yaxis.set_label_coords(-.2, 0.5)
                ax[i].legend(fontsize=font-12, frameon=False)
                ax[i].tick_params(axis='both', which='major', labelsize=font-12)
                ax[i].xaxis.set_label_coords(.5, -.05)
                ax[i].set_xticks(np.linspace(700, 880, 7))
                 # ax[i].set_yticks(np.linspace(0, 1.5e-8, 6))
                ax[i].set_xlabel('Wavelength (nm)', fontsize=font-4)
            
            if nfit ==20:
                ax[i].grid(linestyle='--')
        rmspe = df_para.at[0, 'RMSP']
        fig.suptitle(f'Subject B', fontsize=font-2)
    fig.savefig(os.path.join(folder, 'spec_pics_re', f'fit_all_re.png'), dpi=300)