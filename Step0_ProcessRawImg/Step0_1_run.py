# %%
import numpy as np
import os
import cv2
import pandas as pd
import skimage.io 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from glob import glob
from natsort import natsorted
from tqdm import tqdm
import process_raw as pr
import matplotlib.ticker as mtick
import scienceplots
from scipy import signal

# do not change
SDS_LIST = [4.5, 7.5, 10.5]
CH_LIST = ('ch1', 'ch2', 'ch3')

# %%
#########################################
################ default ################
#########################################

# input folder
ifolder = '20231026_kb'

# The folder you want to process in input folder
subfolder = ['kb_neck']
# subfolder = ['3', '4', '5', '6']
# subfolder = ['kb_arterial']
# subfolder = ['2s', '4s', '6s', '8s', '10s', ]
# subfolder = ['syu_venous']

isOcclusion = False
isPlotEachSpec = False 
isPhantom = False

# if in-vivo, set subject name
subject = 'kb'      # For in vivo

# use to plot
day = '10/26'

# if process occlusion data
occlusion_type = 'venous'   
# occlusion_type = 'arterial'
cycle_time = 3.13788    # occlusion cycle time

# Set output path
ofolder = 'm_out_' + ifolder
ofolder2 = 'Step0_2_Phantom/Step0_2_2_SpectrumCalibration/' + ofolder + '/extracted_spec'
if not os.path.isdir(ofolder):
    os.mkdir(ofolder)
if not os.path.isdir(ofolder2):
    os.makedirs(ofolder2)
if isOcclusion:
    ofolder += f'/{subfolder[0]}'
    ofolder2 += f'/{subfolder[0]}'
    if not os.path.isdir(ofolder):
        os.mkdir(ofolder)
    if not os.path.isdir(ofolder2):
        os.mkdir(ofolder2)
        
# Wavelength calibration factor defined : y = ax + b
# kb 1026, eu 1016, syu 1006
# a = 0.6159696
# b = 357.78707
# a=0.611321
# b=361.92453
a=0.61597
b=357.78707
# kb test
# a=0.6132
# b=331.51

# Choose wavelength range
start_wl = 553
stop_wl = 857
start_wl = 474
stop_wl = 1043

# Choose pixel y range
row_choose = ((74, 80), (119, 131), (163, 182))     # kb 1026
# row_choose = ((63, 76), (110, 123), (155, 170))     # eu 1016
# row_choose = ((66, 74), (113, 124), (87, 172))     # syu 1006
# row_choose = ((74, 83), (119, 132), (165, 182))     # by 1102

# %%
#########################################
############# Process data ##############
#########################################

# %% For multi test
# subfolder = [f'{i}_stability_test' for i in np.arange(1, 11, 1, dtype=np.int64)]
# for subname in tqdm(subfolder):
#     path_det_bg = glob(os.path.join(ifolder, subname, 'background*'))
#     path_det = glob(os.path.join(ifolder, subname, '3*')) 
#     bg_arr, df_det_mean, df_det_ch1, df_det_ch2, df_det_ch3 = pr.get_spec(path_det_bg, path_det, row_choose, a, b, img_size=(200, 160))
#     df_det_mean.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_mean.csv'), index = False)
#     df_det_ch1.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch1.csv'), index = False)
#     df_det_ch2.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch2.csv'), index = False)
#     df_det_ch3.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch3.csv'), index = False)
#     det_list = [df_det_ch1, df_det_ch2, df_det_ch3]

# %% Load target spectrum
for subname in tqdm(subfolder):
    path_det_bg = glob(os.path.join(ifolder, subname, 'background*'))
    path_det_bg = natsorted(path_det_bg)
    # path_det_bg = glob(os.path.join(ifolder, 'background*'))
    # path_det = glob(os.path.join(ifolder, subname, subname + '*')) if isPhantom else glob(os.path.join(ifolder, subname, subject + '*'))
    path_det = glob(os.path.join(ifolder, subname, f'{subname}*')) if isPhantom else glob(os.path.join(ifolder, subname, subject + '*'))
    path_det = natsorted(path_det)
    bg_arr, df_det_mean, df_det_ch1, df_det_ch2, df_det_ch3 = pr.get_spec(path_det_bg, path_det, row_choose, a, b, img_size=(200, 1600), isOcclusion=isOcclusion, cycle_time=3.13788)
        
    # df_det_mean.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_mean.csv'), index = False)
    # df_det_ch1.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch1.csv'), index = False)
    # df_det_ch2.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch2.csv'), index = False)
    # df_det_ch3.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch3.csv'), index = False)
    
    # for shot in range(df_det_ch1.shape[1]-1):
    #     df_det_ch1.iloc[7:-7, shot+1] = pr.moving_average(df_det_ch1.iloc[:, shot+1], 15)
    #     df_det_ch2.iloc[3:-3, shot+1] = pr.moving_average(df_det_ch2.iloc[:, shot+1], 7)
    #     df_det_ch3.iloc[4:-4, shot+1] = pr.moving_average(df_det_ch3.iloc[:, shot+1], 9)
    
    # filter test
    # b, a = signal.butter(8,0.05,'lowpass')
    # bs = signal.filtfilt(b, a, df_det_ch2.loc[start_wl:stop_wl, 'shot_0'])
    # ms = df_det_ch2.copy()
    # ms.iloc[30:-30, 1] = pr.moving_average(df_det_ch2.iloc[:, 1], 61)
    # plt.figure(dpi=300)
    # plt.plot(df_det_ch2.loc[start_wl:stop_wl, 'wl'], df_det_ch2.loc[start_wl:stop_wl, 'shot_0'], label='Raw')
    # plt.plot(df_det_ch2.loc[start_wl:stop_wl, 'wl'], bs, label='Butterworth filter')
    # plt.plot(df_det_ch2.loc[start_wl:stop_wl, 'wl'], ms.loc[start_wl:stop_wl, 'shot_0'], label='Moving average')
    # plt.title('2023/10/16 Phantom 3')
    # plt.xlabel('Wavelength (nm)')
    # plt.ylabel('Intensity (gray value)')
    # plt.grid()
    # plt.legend()
    # plt.savefig('filter_3.png')
    # bf, af = signal.butter(8,0.05,'lowpass')
    # for shot in range(df_det_ch1.shape[1]-1):
    #     df_det_ch1.iloc[start_wl:stop_wl+1, shot+1] = signal.filtfilt(bf, af, df_det_ch1.iloc[start_wl:stop_wl+1, shot+1])
    #     df_det_ch2.iloc[start_wl:stop_wl+1, shot+1] = signal.filtfilt(bf, af, df_det_ch2.iloc[start_wl:stop_wl+1, shot+1])
    #     df_det_ch3.iloc[start_wl:stop_wl+1, shot+1] = signal.filtfilt(bf, af, df_det_ch3.iloc[start_wl:stop_wl+1, shot+1])
    df_det_ch1.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch1.csv'), index = False)
    df_det_ch2.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch2.csv'), index = False)
    df_det_ch3.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_ch3.csv'), index = False)
    
    interp_wl = np.arange(680, 901)
    interp_wl = np.arange(650, 1000)
    
    # 3 channel
    df_det_ch1_interp = pd.DataFrame(np.zeros((interp_wl.size, df_det_ch1.columns.size)), columns=df_det_ch1.columns)
    df_det_ch2_interp = pd.DataFrame(np.zeros((interp_wl.size, df_det_ch2.columns.size)), columns=df_det_ch2.columns)
    df_det_ch3_interp = pd.DataFrame(np.zeros((interp_wl.size, df_det_ch3.columns.size)), columns=df_det_ch3.columns)
    df_det_ch1_interp['wl'] = interp_wl
    df_det_ch2_interp['wl'] = interp_wl
    df_det_ch3_interp['wl'] = interp_wl
    df_mean_interp = pd.DataFrame(
                {'wl': interp_wl,
                 'ch1': np.zeros(interp_wl.size),
                 'ch2': np.zeros(interp_wl.size),
                 'ch3': np.zeros(interp_wl.size)})  
    
    for t in range(df_det_ch1.columns.size-1):
        # df_det_ch1.iloc[start_wl:stop_wl+1, t+1] = signal.filtfilt(bf, af, df_det_ch1.iloc[start_wl:stop_wl+1, t+1])
        # df_det_ch2.iloc[start_wl:stop_wl+1, t+1] = signal.filtfilt(bf, af, df_det_ch2.iloc[start_wl:stop_wl+1, t+1])
        # df_det_ch3.iloc[start_wl:stop_wl+1, t+1] = signal.filtfilt(bf, af, df_det_ch3.iloc[start_wl:stop_wl+1, t+1])
        df_det_ch1_interp.iloc[:, t+1] = np.interp(interp_wl, df_det_ch1['wl'], df_det_ch1.iloc[:, t+1])
        df_det_ch2_interp.iloc[:, t+1] = np.interp(interp_wl, df_det_ch2['wl'], df_det_ch2.iloc[:, t+1])
        df_det_ch3_interp.iloc[:, t+1] = np.interp(interp_wl, df_det_ch3['wl'], df_det_ch3.iloc[:, t+1])
        
    df_det_ch1_interp.to_csv(os.path.join(ofolder, subname+'_det_ch1_interp.csv'), index = False)
    df_det_ch2_interp.to_csv(os.path.join(ofolder, subname+'_det_ch2_interp.csv'), index = False)
    df_det_ch3_interp.to_csv(os.path.join(ofolder, subname+'_det_ch3_interp.csv'), index = False)
    for ch in range(3):
        # df_det_mean.iloc[start_wl:stop_wl+1, ch+1] = signal.filtfilt(bf, af, df_det_mean.iloc[start_wl:stop_wl+1, ch+1])
        df_mean_interp.iloc[:, ch+1] = np.interp(interp_wl, df_det_mean['wl'], df_det_mean.iloc[:, ch+1])
    df_det_mean.loc[start_wl:stop_wl, :].to_csv(os.path.join(ofolder, subname+'_det_mean.csv'), index = False)
    df_mean_interp.to_csv(os.path.join(ofolder, subname+'_det_mean_interp.csv'), index=False)
    
    # To ofolder2
    if isPhantom:
        df_mean_interp.to_csv(os.path.join(ofolder2, 'phantom_p' + subname + '.txt'), index=False, sep='\t', header=False)
    elif isOcclusion:
        df_det_timelist = [pd.DataFrame(np.zeros((interp_wl.size, 4))) for t in range(df_det_ch1.columns.size-1)]
        for t in range(len(df_det_timelist)):
            df_det_timelist[t].iloc[:, 0] = interp_wl
            df_det_timelist[t].iloc[:, 1] = df_det_ch1_interp.iloc[:, t+1]
            df_det_timelist[t].iloc[:, 2] = df_det_ch2_interp.iloc[:, t+1]
            df_det_timelist[t].iloc[:, 3] = df_det_ch3_interp.iloc[:, t+1]
            df_det_timelist[t].to_csv(os.path.join(ofolder2, f'{t:04d}.txt'), index=False, sep='\t', header=False)
        timelist = df_det_ch1_interp.columns[1:].to_list()   
        curdir = os.getcwd()  
        os.chdir(ofolder2)
        os.chdir('../')
        with open('timelist.txt', 'w') as f:
            for token in timelist:
                f.write(token+'\n')
        os.chdir(curdir)
    else:
        df_mean_interp.to_csv(os.path.join(ofolder2, subname+'.txt'), index=False, sep='\t', header=False)      
    det_list = [df_det_ch1_interp, df_det_ch2_interp, df_det_ch3_interp]
    if isOcclusion:
        # ylimit = [(50000, 180000), (30000, 130000), (30000, 160000)]
        # ylimit = [(20000, 140000), (20000, 100000), (20000, 100000)]
        # ylimit = [(0, 1.5), (0, 1.5), (0, 1.5)]
        # ylimit = [(-1.5, 1.5), (-1.5, 1.5), (-1.5, 1.5)]
        fig1, ax1 = plt.subplots(3, 1, dpi=300, figsize=(12, 8))
        fig2, ax2 = plt.subplots(3, 1, dpi=300, figsize=(12, 8))
        for ch in range(3):
            out_specpath = os.path.join(ofolder, str(ch+1))
            if not os.path.isdir(out_specpath):
                os.mkdir(out_specpath)
            df_ch = pd.read_csv(os.path.join(ofolder, subname+f'_det_ch{ch+1}.csv'))
            
            
            # Plot 758, 800, 850 nm
            # df_ch = df_ch.drop(df_ch.columns[list(range(13, 113, 11)) + list(range(113, 169, 11)) + list(range(174, 251, 11))], axis=1)
            # df_ch = df_ch.drop(df_ch.columns[[1, 2]], axis=1)
            time_list = df_ch.columns.to_list()
            time_list = time_list[1:]
            time_list = list(np.float_(time_list))
            # spec_758 = df_ch[df_ch['wl']==758.4584].iloc[0, 1:].squeeze()
            # spec_800 = df_ch[df_ch['wl']==800.5264].iloc[0, 1:].squeeze()
            # spec_850 = df_ch[df_ch['wl']==851.008].iloc[0, 1:].squeeze()
                        
            # df_ch.iloc[:, 1:] /= np.mean(df_ch.iloc[:, 1:], 0)
            spec_758 = df_ch[np.floor(df_ch['wl'])==760].iloc[0, 1:].squeeze()
            spec_800 = df_ch[np.floor(df_ch['wl'])==800].iloc[0, 1:].squeeze()
            spec_850 = df_ch[np.floor(df_ch['wl'])==850].iloc[0, 1:].squeeze()
            # normspec_758 = spec_758 / spec_758[0]
            # normspec_800 = spec_800 / spec_800[0]
            # normspec_850 = spec_850 / spec_850[0]
            delod_758 = -np.log(spec_758 / np.mean(spec_758[:10]))
            delod_800 = -np.log(spec_800 / np.mean(spec_800[:10]))
            delod_850 = -np.log(spec_850 / np.mean(spec_850[:10]))
            ax1[ch].plot(time_list, spec_758, 'b', label=str(760)+' nm')
            ax1[ch].plot(time_list, spec_800, 'g', label=str(800)+' nm')
            ax1[ch].plot(time_list, spec_850, 'r', label=str(850)+' nm')
            ax2[ch].plot(time_list, delod_758, 'b', label=str(760)+' nm')
            ax2[ch].plot(time_list, delod_800, 'g', label=str(800)+' nm')
            ax2[ch].plot(time_list, delod_850, 'r', label=str(850)+' nm')
            # ax[ch].set_xticks(np.linspace(0, 781, 30))
            # ax[ch].xaxis.set_major_locator(plt.MaxNLocator(5))
            if ch == 0:
                if occlusion_type == 'venous':
                    ax1[ch].text(time_list[12], ax1[ch].get_ylim()[1]+0.05, 'Occlusion')
                    ax1[ch].text(time_list[108], ax1[ch].get_ylim()[1]+0.05, 'Release')
                    ax2[ch].text(time_list[12], 0.16, 'Occlusion')
                    ax2[ch].text(time_list[108], 0.16, 'Release')
                else:
                    ax1[ch].text(time_list[12], ax1[ch].get_ylim()[1]+0.05, 'Occlusion')
                    ax1[ch].text(time_list[108], ax1[ch].get_ylim()[1]+0.05, 'Release')
                    ax2[ch].text(time_list[12], 0.18, 'Occlusion')
                    ax2[ch].text(time_list[108], 0.18, 'Release')
            if ch == 2:
                ax1[ch].set_xlabel('Time (secs)', fontsize=14)
                ax1[ch].set_ylabel('Intensity (gray value)', fontsize=14)
                ax1[ch].legend(loc='upper right', bbox_to_anchor=(1.13, 2))
                ax1[ch].yaxis.set_label_coords(-0.1, 1.6)
                ax2[ch].set_xlabel('Time (secs)', fontsize=14)
                ax2[ch].set_ylabel('∆OD', fontsize=14)
                ax2[ch].legend(loc='upper right', bbox_to_anchor=(1.13, 2))
                ax2[ch].yaxis.set_label_coords(-0.1, 1.6)
            ax1[ch].set_title(CH_LIST[ch], rotation='vertical', x=-0.07, y=0.4)
            ax1[ch].grid()
            ax1[ch].axvspan(xmin=58, xmax=60, color='red', alpha=0.3)
            ax1[ch].axvspan(xmin=357, xmax=359, color='blue', alpha=0.3)
            ax1[ch].tick_params(axis='both', which='major', labelsize=10)
            ax2[ch].set_title(CH_LIST[ch], rotation='vertical', x=-0.07, y=0.4)
            # ax2[ch].set_ylim((-0.1, 0.1))
            ax2[ch].grid()
            ax2[ch].axvspan(xmin=58, xmax=60, color='red', alpha=0.3)
            ax2[ch].axvspan(xmin=357, xmax=359, color='blue', alpha=0.3)
            ax2[ch].tick_params(axis='both', which='major', labelsize=10)
        
            # Plot each spectra 
            if isPlotEachSpec:
                time_list = df_ch.columns.to_list()
                time_list = time_list[1:]
                time_list = list(np.float_(time_list))
                for id, time in tqdm(enumerate(time_list)):
                    plt.figure(dpi=300)
                    # if ch!=2:
                    #     plt.plot(df_ch.loc[5:288, 'wl'], pr.moving_average(df_ch.iloc[:, id+1], 11))
                    # else:
                    #     # break
                    plt.plot(df_ch.loc[5:288, 'wl'], df_ch.iloc[5:289, id+1])
                    # plt.ylim(ylimit[ch])
                    plt.xlabel('Wavelength (nm)')
                    plt.ylabel('Intensity (gray value)')
                    plt.title(f'{float(time):.1f} secs')
                    plt.grid()
                    plt.tight_layout()
                    plt.savefig(os.path.join(out_specpath, f'{id:04d}.png'))    
            
            # Plot delta OD
        if occlusion_type == 'venous':
            fig1.suptitle(f'Venous occlusion, {day} subject {subject}', fontsize=18)
            fig2.suptitle(f'Venous occlusion, {day} subject {subject}', fontsize=18)
        else:
            fig1.suptitle(f'Arterial occlusion, {day} subject {subject}', fontsize=18)
            fig2.suptitle(f'Arterial occlusion, {day} subject {subject}', fontsize=18)
        fig1.savefig(os.path.join(ofolder, f'feature.png')) 
        fig2.savefig(os.path.join(ofolder, f'feature_od.png')) 
    else:
        stat_list = pr.get_stat(det_list, 0, det_list[0].shape[0]-1)
        fig, ax = plt.subplots(1, 3, figsize=(12, 6))
        # fig, ax = plt.subplots(1, 3)
        font = 16
        for i in range(3):
            for j in range(df_det_ch1.shape[1]-1):
                ax[i].plot(det_list[i].loc[:, 'wl'], det_list[i].loc[:, f'shot_{j}'])
            ax[i].set_title(f'SDS = {SDS_LIST[i]} mm', fontsize=font)
            # ax[i].set_xticks(np.arange(700, 881, 30))
            if i == 1:
                ax[i].set_xlabel('Wavelength (nm)', fontsize=font)
            if i == 0:
                ax[i].set_ylabel('Intensity (counts)', fontsize=font)
            ax[i].tick_params(axis='both', which='major', labelsize=font-4)
            ax2 = ax[i].twinx()
            ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f%%'))
            ax2.plot(stat_list[i]['wl'], 100 * stat_list[i]['cv'], color='black', linestyle='--')
            if i == 2:
                ax2.set_ylabel('CV', fontsize=font)
            # ax2.set_yticks(np.linspace(0, 10, 6))
            ax2.tick_params(axis='y')
            ax[i].grid(linestyle='--')
        if isPhantom:    
            fig.suptitle(f'Phantom {subname}', fontsize=font)
        else:
            fig.suptitle(f'Subject {subname}', fontsize=font)
        fig.tight_layout()
        fig.savefig(os.path.join(ofolder, f'{subname}.png'), dpi=300)


# Write video
# if isOcclusion:
#     for ch in range(3):
#         # 设置输入图像文件夹和输出视频文件的路径
#         input_folder = os.path.join(ofolder, str(ch+1))
#         output_video = ofolder + f'/ch{ch+1}.mp4'

#         # 获取输入文件夹中的所有图像文件
#         image_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

#         # 获取第一张图像的宽度和高度以用于创建输出视频
#         first_image = cv2.imread(image_files[0])
#         height, width, layers = first_image.shape

#         # 初始化视频写入器
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 可根据需要选择视频编解码器
#         out = cv2.VideoWriter(output_video, fourcc, 10, (width, height))

#         # 逐个读取图像并将其写入视频
#         for image_file in image_files:
#             frame = cv2.imread(image_file)
#             out.write(frame)

#         # 完成后释放资源
#         out.release()
#         cv2.destroyAllWindows()





# for subname in tqdm(subfolder):
#     df_ch1 = pd.read_csv(os.path.join(ofolder, f'{subname}_det_ch1.csv'))
#     df_ch2 = pd.read_csv(os.path.join(ofolder, f'{subname}_det_ch2.csv'))
#     df_ch3 = pd.read_csv(os.path.join(ofolder, f'{subname}_det_ch3.csv'))
#     df_ch1 = df_ch1.iloc[:, 1:]
#     df_ch2 = df_ch2.iloc[:, 1:]
#     df_ch3 = df_ch3.iloc[:, 1:]
#     cvp_ch1 = 1 / df_ch1.sum(axis=0)
#     cvp_ch2 = 1 / df_ch2.sum(axis=0)
#     cvp_ch3 = 1 / df_ch3.sum(axis=0)

#     # 設定影片參數
#     fps = 30  # 影片每秒幀數
#     duration = 10  # 影片持續時間（秒）
#     num_frames = fps * duration  # 影片總幀數

#     # 隨機產生數據
#     data1 = cvp_ch1.values
#     data2 = cvp_ch2.values
#     data3 = cvp_ch3.values

#     # 創建圖形和軸
#     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 8))

#     # 初始化圖形
#     line1, = ax1.plot([], [], 'r-')
#     line2, = ax2.plot([], [], 'g-')
#     line3, = ax3.plot([], [], 'b-')

#     # 設定圖形範圍
#     ax1.set_xlim(0, num_frames)
#     ax1.set_ylim(0.25e-5, 1.25e-5)
#     ax2.set_xlim(0, num_frames)
#     ax2.set_ylim(0.5e-5, 1.5e-5)
#     ax3.set_xlim(0, num_frames)
#     ax3.set_ylim(0.1e-5, 0.4e-5)
#     ax1.set_ylabel('1 / total R')
#     ax2.set_ylabel('1 / total R')
#     ax3.set_ylabel('1 / total R')
#     ax3.set_xlabel('Frame')
    
#     # 設定主標題
#     # fig.suptitle('1 / total R', fontsize=14)

#     # 設定子圖的標題
#     ax1.set_title('SDS = 4.5 mm')
#     ax2.set_title('SDS = 7.5 mm')
#     ax3.set_title('SDS = 10.5 mm')
    
#     plt.tight_layout()
    
#     # 更新函數，用於每一幀的圖形更新
#     def update(frame):
#         # 獲取當前幀的數據
#         current_data1 = data1[frame]
#         current_data2 = data2[frame]
#         current_data3 = data3[frame]

#         # 更新圖形
#         x = np.arange(frame)

#         y1 = data1[:frame]
#         line1.set_data(x, y1)

#         y2 = data2[:frame]
#         line2.set_data(x, y2)

#         y3 = data3[:frame]
#         line3.set_data(x, y3)

#         return line1, line2, line3

#     # 創建動畫
#     ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=1000/fps, blit=True)

#     # 輸出為影片
#     ani.save(os.path.join(ofolder, f'{subname}_CVP.mp4'), writer='ffmpeg', fps=fps)

#     # 顯示影片
#     # plt.show()









# %% Plot raw data, normalized spectra
# sds_dis = [4.56, 7.49, 10.55]
# for subname in subfolder:
#     fig, ax = plt.subplots(3, 3, figsize=(16, 12), dpi=300)
#     df_det_mean = pd.read_csv(os.path.join(ofolder, subname+'_det_mean.csv'))
#     df_rel_mean = pd.read_csv(os.path.join(ofolder, subname+'_response_mean.csv'))
#     df_ref_mean = pd.read_csv(os.path.join(ofolder, subname+'_reflectance_mean.csv'))
#     for sds in range(3):
#         ax[0, sds].plot(df_det_mean['wl'], df_det_mean[f'ch{sds+1}_mean'])
#         ax[1, sds].plot(df_rel_mean['wl'], df_rel_mean[f'ch{sds+1}_mean'])
#         ax[2, sds].plot(df_ref_mean['wl'], df_ref_mean[f'ch{sds+1}_mean'])
#         ax[0, sds].set_title(f'SDS = {sds_dis[sds]} mm')
#         ax[1, sds].set_title(f'SDS = {sds_dis[sds]} mm')
#         ax[2, sds].set_title(f'SDS = {sds_dis[sds]} mm')
#         ax[0, sds].set_xlabel('Wavelength [nm]')
#         ax[1, sds].set_xlabel('Wavelength [nm]')
#         ax[2, sds].set_xlabel('Wavelength [nm]')
#         ax[0, sds].set_ylabel('Gray value [counts]')
#         ax[1, sds].set_ylabel('Relative response [counts]')
#         ax[2, sds].set_ylabel('Normalized intensity [-]')
#         ax[0, sds].grid(visible=True)
#         ax[1, sds].grid(visible=True)
#         ax[2, sds].grid(visible=True)
#     fig.suptitle(f'Phantom {subname}')
#     fig.tight_layout()
#     fig.savefig(os.path.join(ofolder, subname+'.png'))
# print('Finished !\n')