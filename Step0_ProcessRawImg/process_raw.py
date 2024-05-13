"""
This script provide some useful function to process raw spectra
"""

import numpy as np
import os
import pandas as pd
import skimage.io 
import matplotlib.pyplot as plt
from glob import glob

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def get_spec(path_background, path_tar, row_choose, a, b, *, img_size=(200, 1600), isOcclusion=False, cycle_time=3.13788): 
    """_summary_

    Args:
        path_background (_type_): _description_
        path_tar (_type_): _description_
        row_choose (_type_): _description_
        a (_type_): _description_
        b (_type_): _description_
        img_size (tuple, optional): _description_. Defaults to (200, 1600).

    Returns:
        list: [img_background, dfmean, df_chN...]
    """
    img_background = np.zeros(img_size, dtype = 'float64')
    tar_list = len(path_tar) * [np.zeros(img_size, dtype = 'float64')]
    
    # Calculate BG means
    for bgid in range(len(path_background)):
        img_background += skimage.io.imread(path_background[bgid], plugin = 'tifffile').astype(np.float64) 
    img_background /= len(path_background)
    
    # If forget BG
    # row1 = list(range(57, 71))
    # row2 = list(range(100, 120))
    # row3 = list(range(142, 175))
    # img_background[[row1+row2+row3], :] = img_background[83, :]
    
    # Each shot substract mean BG
    for tarid in range(len(path_tar)):
        tar_list[tarid] = skimage.io.imread(path_tar[tarid], plugin = 'tifffile').astype(np.float64) 
        tar_list[tarid] -= img_background
        tar_list[tarid][tar_list[tarid] < 0] = 0
        
    # Split in 3 channel           
    tar_ch_list = []        # ch1, 2, 3
    for chid in range(len(row_choose)):
        # axis 0: each shot; axis 1: wl
        temp_arr = np.zeros((len(path_tar), img_size[1]))
        for tarid in range(len(path_tar)):
            row_tar = np.sum(tar_list[tarid][row_choose[chid][0] : row_choose[chid][1], :], 0)
            temp_arr[tarid, :] = row_tar
        tar_ch_list.append(temp_arr)
    
    # Process output
    df_temp = pd.DataFrame(np.array([np.arange(img_size[1])]).T, columns=['wl'])
    # df_temp = a * (2*df_temp) + b
    df_temp = a * df_temp + b
    
    # each channel mean
    dmean = {f'ch{i+1}_mean': np.mean(tar_ch_list[i], 0) for i in range(len(row_choose))}
    dfmean = pd.DataFrame(data=dmean, dtype='float64')
    dfmean = pd.concat([df_temp, dfmean], axis = 1)
    out = [img_background, dfmean]
    
    # each channel
    for chid in range(len(row_choose)):
        if isOcclusion:
            d = {f'{i*cycle_time}': tar_ch_list[chid][i, :] for i in range(len(tar_ch_list[chid]))}
        else:
            d = {f'shot_{i}': tar_ch_list[chid][i, :] for i in range(len(tar_ch_list[chid]))}
        df = pd.DataFrame(data=d, dtype='float64')
        df = pd.concat([df_temp, df], axis = 1)
        out.append(df)
    return out

# No needed below
# 
# 
# 
# 
def getRelative_response(det_list, df_src_mean):
    # fiber_area = [25**2, 52.5**2, 100**2]
    for chid in range(len(det_list)):
        for shot in range(det_list[chid].shape[1]-1):
            det_list[chid].iloc[:, shot+1] /= df_src_mean.iloc[:, chid+1]
            # det_list[chid].iloc[:, shot+1] /= fiber_area[chid]
    df_temp = det_list[0]['wl']
    dmean = {f'ch{i+1}_mean': np.mean(det_list[i].iloc[:, 1:].values, 1) for i in range(len(det_list))}
    dfmean = pd.DataFrame(data=dmean, dtype='float64')
    dfmean = pd.concat([df_temp, dfmean], axis = 1)
    return det_list, dfmean

def getNormalize_reflectance(rel_list, start_wl, stop_wl, /, ref_fiber=1):
    mean_intensity = np.mean(rel_list[ref_fiber-1].loc[start_wl:stop_wl, 'shot_0':], 0)
    for i in range(len(rel_list)):
        rel_list[i].loc[start_wl:stop_wl, 'shot_0':] /= mean_intensity
    df_temp = rel_list[0]['wl']
    dmean = {f'ch{i+1}_mean': np.mean(rel_list[i].iloc[:, 1:].values, 1) for i in range(len(rel_list))}
    dfmean = pd.DataFrame(data=dmean, dtype='float64')
    dfmean = pd.concat([df_temp, dfmean], axis = 1)
    return rel_list, dfmean

def get_stat(ref_list, start_wl, stop_wl):
    stat_list = []
    for i in range(len(ref_list)):
        # get average, standard deviation and CV
        avg = ref_list[i].loc[start_wl:stop_wl, 'shot_0':].mean(axis=1)
        std = ref_list[i].loc[start_wl:stop_wl, 'shot_0':].std(axis=1)
        cv = std / avg    
        d = {'wl': ref_list[i].loc[start_wl:stop_wl, 'wl'], 'avg': avg, 'std': std, 'cv': cv}
        df_stat = pd.DataFrame(d)
        stat_list.append(df_stat)
        
    return stat_list

def plotNoise_pattern(df, chname, figname, start_wl, stop_wl):
    index = np.floor(np.linspace(start_wl, stop_wl, 6))
    plt.figure(dpi=300)
    plt.suptitle(chname)
    plt.subplot(231)
    wl = int(df.loc[int(index[0]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[0]), 1:])
    plt.subplot(232)
    wl = int(df.loc[int(index[1]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[1]), 1:])
    plt.subplot(233)
    wl = int(df.loc[int(index[2]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[2]), 1:])
    plt.subplot(234)
    wl = int(df.loc[int(index[3]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[3]), 1:])
    plt.subplot(235)
    wl = int(df.loc[int(index[4]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[4]), 1:])
    plt.subplot(236)
    wl = int(df.loc[int(index[5]), 'wl'])
    plt.title(str(wl) + ' nm')
    plt.xlabel('Normalized reflectance')
    plt.ylabel('Counts')
    plt.hist(df.iloc[int(index[5]), 1:])
    
    plt.tight_layout()
    plt.savefig(figname)
            