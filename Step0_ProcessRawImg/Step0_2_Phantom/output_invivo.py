
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# typical 
subject = '20231016_eu_sr2'
ofilepath = os.path.join('InvivoReflectance', subject)
invivofolder = 'm_out_20231016_eu'
invivoname = 'eu_neck_det_mean_interp.csv'
invivofolder = os.path.join('MeasureData', invivofolder)
# phantomfolder = 'm_out_20230812'
regpath = os.path.join('AbsCalibration', '3sr_4sr_5sr_6_m_out_20231016_eu_fromExp2', 'reg.csv')
df_invivo = pd.read_csv(os.path.join(invivofolder, invivoname))
# df_invivo_std = pd.read_csv(os.path.join(invivofolder, 'standard-0.04_det_mean.csv'))
# df_ph_std = pd.read_csv(os.path.join(phantomfolder, 'standard-0.04_det_mean.csv'))
df_reg = pd.read_csv(regpath)
# power_phactor = df_ph_std.iloc[:, 1:].values / df_invivo_std.iloc[:, 1:].values
# df_invivo.iloc[:, 1:] *= power_phactor

wl = df_reg['wl']
d = {'wl': wl,
     'ch1': np.interp(wl, df_invivo['wl'], df_invivo['ch1']),
     'ch2': np.interp(wl, df_invivo['wl'], df_invivo['ch2']),
     'ch3': np.interp(wl, df_invivo['wl'], df_invivo['ch3'])}
df_invivo_interp = pd.DataFrame(d)
for ch in range(3):
    df_invivo_interp.iloc[:, ch+1] *= df_reg[f'{ch+1}a']
    df_invivo_interp.iloc[:, ch+1] += df_reg[f'{ch+1}b']
df_invivo_interp.to_csv(ofilepath+'.csv', index=False)
df_invivo_interp.to_csv(ofilepath+'.txt', index=False, sep='\t', header=None)

# realtime
# subject = 'syu_arterial_20231006'
# ofilepath = os.path.join('InvivoReflectance', subject)
# invivofolder = 'm_out_20231006_occlusion/syu_arterial'
# invivoname = ['syu_arterial_det_ch1.csv', 'syu_arterial_det_ch2.csv', 'syu_arterial_det_ch3.csv']
# invivofolder = os.path.join('MeasureData', invivofolder)
# # phantomfolder = 'm_out_20230812'
# regpath = os.path.join('AbsCalibration', '3456_m_out_20231006_occlusion_sout_1e9_flattop', 'reg.csv')
# df_invivo = []

# if not os.path.exists(ofilepath):
#     os.mkdir(ofilepath)
# for chname in invivoname:
#     df_invivo.append(pd.read_csv(os.path.join(invivofolder, chname)))

# # df_invivo_std = pd.read_csv(os.path.join(invivofolder, 'standard-0.04_det_mean.csv'))
# # df_ph_std = pd.read_csv(os.path.join(phantomfolder, 'standard-0.04_det_mean.csv'))
# df_reg = pd.read_csv(regpath)
# # power_phactor = df_ph_std.iloc[:, 1:].values / df_invivo_std.iloc[:, 1:].values
# # df_invivo.iloc[:, 1:] *= power_phactor
# wl = df_reg['wl']
# df_invivo_all = []
# for ch in range(3):
#     temp_arr = np.zeros((wl.size, df_invivo[ch].shape[1]))
#     df_invivo_interp = pd.DataFrame(temp_arr, columns=df_invivo[ch].columns)
#     for time in range(df_invivo_interp.shape[1]-1):
#         df_invivo_interp.iloc[:, time+1] = np.interp(wl, df_invivo[ch]['wl'], df_invivo[ch].iloc[:, time+1])
#     # df_invivo_interp = pd.concat([df_reg[['wl']], df_invivo_interp], axis=1)
#     df_invivo_interp.iloc[:, 1:] = df_invivo_interp.iloc[:, 1:].mul(df_reg[f'{ch+1}a'], axis=0)
#     df_invivo_interp.iloc[:, 1:] = df_invivo_interp.iloc[:, 1:].add(df_reg[f'{ch+1}b'], axis=0)
#     # df_invivo_interp = df_invivo_interp.drop(df_invivo_interp.columns[list(range(13, 113, 11)) + list(range(113, 169, 11)) + list(range(174, 251, 11))], axis=1)
#     # df_invivo_interp = df_invivo_interp.drop(df_invivo_interp.columns[[1, 2]], axis=1)
#     df_invivo_all.append(df_invivo_interp)
# wl = df_reg[['wl']]
# for time in range(df_invivo_all[0].shape[1]-1):
#     dft = pd.concat([wl, df_invivo_all[0].iloc[:, time+1], df_invivo_all[1].iloc[:, time+1], df_invivo_all[2].iloc[:, time+1]], axis=1)
#     dft.to_csv(os.path.join(ofilepath, f'{time}.txt'), index=False, sep='\t', header=None)
#     # df_invivo_interp.to_csv(ofilepath+'.csv', index=False)
#     # df_invivo_interp.to_csv(ofilepath+'.txt', index=False, sep='\t', header=None)
