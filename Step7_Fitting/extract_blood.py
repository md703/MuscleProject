import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from scipy.ndimage import uniform_filter1d
from glob import glob
from natsort import natsorted
from numpy.linalg import norm
from sklearn import manifold, datasets
from sklearn.decomposition import PCA

window_size = 5
# window_size = 13 
person = 2
oc = 2
posfix = 'lowest_no_restriction'
outpath = os.path.join('Fig', posfix)

if not os.path.exists(outpath):
    os.makedirs(outpath)
    
# if person == 1:
#     day = '10/06'
#     subject = 'syu'
#     if oc == 1:
#         folder = 'syu_arterial_1006_dilated'
#         ofilename = f'syu_arterial_1006_dilated{posfix}'
#     elif oc == 2:
#         folder = 'syu_venous_1006_dilated'
#         ofilename = f'syu_venous_1006_dilated_{posfix}'
# elif person == 2:
#     day = '10/16'
#     subject = 'eu'
#     if oc == 1:
#         folder = 'eu_arterial_1016_dilated'
#         ofilename = f'eu_arterial_1016_dilated_{posfix}'
#     elif oc ==2:
#         folder = 'eu_venous_1016_dilated'
#         ofilename = f'eu_venous_1016_dilated_{posfix}'
# elif person ==3:
#     day = '10/26'
#     subject = 'kb'
#     if oc == 1:
#         folder = 'kb_arterial_1026_dilated'
#         ofilename = f'kb_arterial_1026_dilated_{posfix}'
#     elif oc ==2:
#         folder = 'kb_venous_1026_dilated'
#         ofilename = f'kb_venous_1026_dilated_{posfix}'
if person == 1:
    day = '10/06'
    subject = 'syu'
    if oc == 1:
        folder = 'syu_arterial_1006_dilated_3stage_new'
        ofilename = f'syu_arterial_1006_dilated_3stage_new{posfix}'
    elif oc == 2:
        folder = 'syu_venous_1006_dilated_3stage_new'
        ofilename = f'syu_venous_1006_dilated_3stage_new{posfix}'
elif person == 2:
    day = '10/16'
    subject = 'eu'
    if oc == 1:
        folder = 'eu_arterial_1016_dilated_3stage_new'
        ofilename = f'eu_arterial_1016_dilated_3stage_new{posfix}'
    elif oc ==2:
        folder = 'eu_venous_1016_dilated_3stage_new'
        ofilename = f'eu_venous_1016_dilated_3stage_new{posfix}'
elif person ==3:
    day = '10/26'
    subject = 'kb'
    if oc == 1:
        folder = 'kb_arterial_1026_dilated_3stage_new'
        ofilename = f'kb_arterial_1026_dilated_3stage_new{posfix}'
    elif oc ==2:
        folder = 'kb_venous_1026_dilated_3stage_new'
        ofilename = f'kb_venous_1026_dilated_3stage_new{posfix}'

if oc == 1:
    occlusion_type = 'arterial occlusion'
elif oc == 2:
    occlusion_type = 'venous occlusion'
    
tpath = glob(os.path.join(folder, '*'))
tpath = natsorted(tpath)
df_time = pd.read_csv('Invivo/timelist.txt', names=['time'])

df_all = pd.DataFrame(np.zeros((len(tpath), 8)), columns=['time', 'Chb2', 'alpha2','Chb3', 'alpha3','Chb4', 'alpha4', 'RMSP'])

for t, id_tpath in enumerate(tpath):
    fitpath = os.path.join(id_tpath, 'fit_res.csv')
    df_fit = pd.read_csv(fitpath)
    df_fit['Chb2'] /= 64500
    df_fit['Chb3'] /= 64500
    df_fit['Chb4'] /= 64500
    
    # # choose RMSP lowest
    # # criteria = (df_fit['alpha2']<=0.9) & (df_fit['alpha2']>=0.5) & (df_fit['alpha3']<=0.9) & (df_fit['alpha3']>=0.5) & (df_fit['alpha4']<=0.9) & (df_fit['alpha4']>=0.5)
    # # df_fit = df_fit.loc[criteria, :]
    df_fit = df_fit.sort_values(['RMSP'])
    # df_fit = df_fit[(df_fit['RMSP']-df_fit.loc[0, 'RMSP']) <= 1 ]
    df_all.loc[t, 'Chb2'] =  df_fit.loc[0, 'Chb2']
    df_all.loc[t, 'Chb3'] =  df_fit.loc[0, 'Chb3']
    df_all.loc[t, 'Chb4'] =  df_fit.loc[0, 'Chb4']
    df_all.loc[t, 'alpha2'] =  df_fit.loc[0, 'alpha2']
    df_all.loc[t, 'alpha3'] =  df_fit.loc[0, 'alpha3']
    df_all.loc[t, 'alpha4'] =  df_fit.loc[0, 'alpha4']
    df_all.loc[t, 'RMSP'] =  df_fit.loc[0, 'RMSP']
    
    df_fit['HbO_dermis'] = df_fit['Chb2'].values * df_fit['alpha2'].values
    df_fit['HbR_dermis'] = df_fit['Chb2'].values * (1-df_fit['alpha2']).values
    df_fit['HbO_subcu'] = df_fit['Chb3'].values * df_fit['alpha3'].values
    df_fit['HbR_subcu'] = df_fit['Chb3'].values * (1-df_fit['alpha3']).values
    df_fit['HbO_muscle'] = df_fit['Chb4'].values * df_fit['alpha4'].values
    df_fit['HbR_muscle'] = df_fit['Chb4'].values * (1-df_fit['alpha4']).values
    
    # criteria = (df_fit['RMSP']-df_fit.loc[0,'RMSP']<=1) & (df_fit['RMSP']<=10)
    # df_choose = df_fit[criteria.to_numpy()]
    # df_all.loc[t, 'HbO_dermis_low'] =  df_choose['HbO_dermis'].min()
    # df_all.loc[t, 'HbR_dermis_low'] =  df_choose['HbR_dermis'].min()
    # df_all.loc[t, 'HbO_subcu_low'] =  df_choose['HbO_subcu'].min()
    # df_all.loc[t, 'HbR_subcu_low'] =  df_choose['HbR_subcu'].min()
    # df_all.loc[t, 'HbO_muscle_low'] =  df_choose['HbO_muscle'].min()
    # df_all.loc[t, 'HbR_muscle_low'] =  df_choose['HbR_muscle'].min()
    
    # df_all.loc[t, 'HbO_dermis_up'] =  df_choose['HbO_dermis'].max()
    # df_all.loc[t, 'HbR_dermis_up'] =  df_choose['HbR_dermis'].max()
    # df_all.loc[t, 'HbO_subcu_up'] =  df_choose['HbO_subcu'].max()
    # df_all.loc[t, 'HbR_subcu_up'] =  df_choose['HbR_subcu'].max()
    # df_all.loc[t, 'HbO_muscle_up'] =  df_choose['HbO_muscle'].max()
    # df_all.loc[t, 'HbR_muscle_up'] =  df_choose['HbR_muscle'].max()
    
    # df_all.loc[t, 'RMSP'] =  df_fit.loc[0, 'RMSP']
     
    # df_all.loc[t, 'Chb_total'] = df_all.loc[t, 'Chb2'] + df_all.loc[t, 'Chb3'] + df_all.loc[t, 'Chb4']
    # df_all.loc[t, 'alpha_total'] = (df_all.loc[t, 'Chb2']*df_all.loc[t, 'alpha2'] + df_all.loc[t, 'Chb3']*df_all.loc[t, 'alpha3'] + df_all.loc[t, 'Chb4']*df_all.loc[t, 'alpha4']) / df_all.loc[t, 'Chb_total']
     
    # choose from t-1 cosine
    # df_fit = df_fit.drop([9])
    # if t == 0:
    #     df_fit = df_fit.sort_values(['RMSP'])
    #     df_all.loc[t, 'Chb2'] =  df_fit.loc[0, 'Chb2']
    #     df_all.loc[t, 'Chb3'] =  df_fit.loc[0, 'Chb3']
    #     df_all.loc[t, 'Chb4'] =  df_fit.loc[0, 'Chb4']
    #     df_all.loc[t, 'alpha2'] =  df_fit.loc[0, 'alpha2']
    #     df_all.loc[t, 'alpha3'] =  df_fit.loc[0, 'alpha3']
    #     df_all.loc[t, 'alpha4'] =  df_fit.loc[0, 'alpha4']
    #     df_all.loc[t, 'RMSP'] =  df_fit.loc[0, 'RMSP']
    # else:
    #     df_temp = df_all.loc[t-1, 'Chb2':'alpha4']
    #     df_t = df_fit.loc[:, 'Chb2':'alpha4']
    #     cosine = np.dot(df_t,df_temp)/(norm(df_t)*norm(df_temp))
    #     index = np.where(cosine == cosine.min())
    #     index = index[0][0]
    #     df_all.loc[t, 'Chb2'] =  df_fit.loc[index, 'Chb2']
    #     df_all.loc[t, 'Chb3'] =  df_fit.loc[index, 'Chb3']
    #     df_all.loc[t, 'Chb4'] =  df_fit.loc[index, 'Chb4']
    #     df_all.loc[t, 'alpha2'] =  df_fit.loc[index, 'alpha2']
    #     df_all.loc[t, 'alpha3'] =  df_fit.loc[index, 'alpha3']
    #     df_all.loc[t, 'alpha4'] =  df_fit.loc[index, 'alpha4']
    #     df_all.loc[t, 'RMSP'] =  df_fit.loc[index, 'RMSP']
    #     pass
    
    # choose from t-1 euclidean
    # df_fit = df_fit.drop([9])
    # if t == 0:
    #     df_fit = df_fit.sort_values(['RMSP'])
    #     df_all.loc[t, 'Chb2'] =  df_fit.loc[0, 'Chb2']
    #     df_all.loc[t, 'Chb3'] =  df_fit.loc[0, 'Chb3']
    #     df_all.loc[t, 'Chb4'] =  df_fit.loc[0, 'Chb4']
    #     df_all.loc[t, 'alpha2'] =  df_fit.loc[0, 'alpha2']
    #     df_all.loc[t, 'alpha3'] =  df_fit.loc[0, 'alpha3']
    #     df_all.loc[t, 'alpha4'] =  df_fit.loc[0, 'alpha4']
    #     df_all.loc[t, 'RMSP'] =  df_fit.loc[0, 'RMSP']
    # else:
    #     df_temp = df_all.loc[t-1, 'Chb2':'alpha4']
    #     df_t = df_fit.loc[:, 'Chb2':'alpha4']
    #     dist = np.linalg.norm(df_t-df_temp, axis=1)
    #     index = np.where(dist == dist.min())
    #     index = index[0][0]
    #     df_all.loc[t, 'Chb2'] =  df_fit.loc[index, 'Chb2']
    #     df_all.loc[t, 'Chb3'] =  df_fit.loc[index, 'Chb3']
    #     df_all.loc[t, 'Chb4'] =  df_fit.loc[index, 'Chb4']
    #     df_all.loc[t, 'alpha2'] =  df_fit.loc[index, 'alpha2']
    #     df_all.loc[t, 'alpha3'] =  df_fit.loc[index, 'alpha3']
    #     df_all.loc[t, 'alpha4'] =  df_fit.loc[index, 'alpha4']
    #     df_all.loc[t, 'RMSP'] =  df_fit.loc[index, 'RMSP']
    #     pass
    
    # choose ga init
    # df_all.loc[t, 'Chb2'] =  df_fit.loc[9, 'Chb2']
    # df_all.loc[t, 'Chb3'] =  df_fit.loc[9, 'Chb3']
    # df_all.loc[t, 'Chb4'] =  df_fit.loc[9, 'Chb4']
    # df_all.loc[t, 'alpha2'] =  df_fit.loc[9, 'alpha2']
    # df_all.loc[t, 'alpha3'] =  df_fit.loc[9, 'alpha3']
    # df_all.loc[t, 'alpha4'] =  df_fit.loc[9, 'alpha4']
    # df_all.loc[t, 'RMSP'] =  df_fit.loc[9, 'RMSP'] 
    
    # choose from t-1 spec most similar
    # if t == 0:
    #     df_fit = df_fit.sort_values(['RMSP'])
    #     index = df_fit.index[0]
    #     pre_spec = pd.read_csv(os.path.join(id_tpath, f'fit_all{index+1}', 'lsqSpec_final.txt'), header=None, sep='   ')
    # else:
    #     spec_list = []
    #     df_rmsp = pd.DataFrame(np.zeros((9, 1)), columns=['RMSP'])
    #     for fitid in range(9):
    #         spec = pd.read_csv(os.path.join(id_tpath, f'fit_all{fitid+1}', 'lsqSpec_final.txt'), header=None, sep='   ')
    #         rmsp = np.sqrt(np.sum(np.sum(((spec-pre_spec)/pre_spec)**2)) / spec.size)
    #         df_rmsp.iloc[fitid] = rmsp
    #         spec_list.append(spec)
    #     df_rmsp = df_rmsp.sort_values(['RMSP'])
    #     index = df_rmsp.index[0]
    #     pre_spec = spec_list[index]
    # df_all.loc[t, 'Chb2'] =  df_fit.loc[index, 'Chb2']
    # df_all.loc[t, 'Chb3'] =  df_fit.loc[index, 'Chb3']
    # df_all.loc[t, 'Chb4'] =  df_fit.loc[index, 'Chb4']
    # df_all.loc[t, 'alpha2'] =  df_fit.loc[index, 'alpha2']
    # df_all.loc[t, 'alpha3'] =  df_fit.loc[index, 'alpha3']
    # df_all.loc[t, 'alpha4'] =  df_fit.loc[index, 'alpha4']
    # df_all.loc[t, 'RMSP'] =  df_fit.loc[index, 'RMSP']  
    
    # choose from t-1 chb2 most similar
    # if t == 0:
    #     df_fit = df_fit.sort_values(['RMSP'])
    #     index = df_fit.index[0]
    #     pre_chb2 = df_fit.loc[index, 'Chb2']
    # else:
    #     df_err = pd.DataFrame(np.zeros((9, 1)), columns=['RMSP'])
    #     for fitid in range(9):
    #         err = abs(df_fit.loc[fitid, 'Chb2']-pre_chb2)
    #         df_err.iloc[fitid] = err
    #     df_err = df_err.sort_values(['RMSP'])
    #     index = df_err.index[0]
    #     pre_chb2 = df_fit.loc[index, 'Chb2']
    # df_all.loc[t, 'Chb2'] =  df_fit.loc[index, 'Chb2']
    # df_all.loc[t, 'Chb3'] =  df_fit.loc[index, 'Chb3']
    # df_all.loc[t, 'Chb4'] =  df_fit.loc[index, 'Chb4']
    # df_all.loc[t, 'alpha2'] =  df_fit.loc[index, 'alpha2']
    # df_all.loc[t, 'alpha3'] =  df_fit.loc[index, 'alpha3']
    # df_all.loc[t, 'alpha4'] =  df_fit.loc[index, 'alpha4']
    # df_all.loc[t, 'RMSP'] =  df_fit.loc[index, 'RMSP']  
    
    # Prepare the data
    #t-SNE
    
    # pca = PCA(n_components=2)
    # newX = pca.fit_transform(df_fit.iloc[:, 4:10])
    # #Data Visualization
    # point_id = [i for i in range(newX.shape[0])]
    # plt.figure()
    # plt.scatter(newX[:, 0], newX[:, 1])
    # for i, txt in enumerate(point_id):
    #     plt.annotate(str(txt), (newX[i, 0], newX[i, 1]))
    # plt.show()
    
    # choose spec similar to previous fit
    pass
    
df_all['Chb2'] = signal.medfilt(df_all['Chb2'], window_size)
df_all['Chb3'] = signal.medfilt(df_all['Chb3'], window_size)
df_all['Chb4'] = signal.medfilt(df_all['Chb4'], window_size)
df_all['alpha2'] = signal.medfilt(df_all['alpha2'], window_size)
df_all['alpha3'] = signal.medfilt(df_all['alpha3'], window_size)
df_all['alpha4'] = signal.medfilt(df_all['alpha4'], window_size)
df_all = df_all.loc[:211, :]
# df_all['Chb2'] = uniform_filter1d(df_all['Chb2'], window_size, mode='nearest')
# df_all['Chb3'] = uniform_filter1d(df_all['Chb3'], window_size, mode='nearest')
# df_all['Chb4'] = uniform_filter1d(df_all['Chb4'], window_size, mode='nearest')
# df_all['alpha2'] = uniform_filter1d(df_all['alpha2'], window_size, mode='nearest')
# df_all['alpha3'] = uniform_filter1d(df_all['alpha3'], window_size, mode='nearest')
# df_all['alpha4'] = uniform_filter1d(df_all['alpha4'], window_size, mode='nearest')

# df_all['HbO_dermis_low'] = uniform_filter1d(df_all['HbO_dermis_low'], window_size, mode='nearest')
# df_all['HbR_dermis_low'] = uniform_filter1d(df_all['HbR_dermis_low'], window_size, mode='nearest')
# df_all['HbO_subcu_low'] = uniform_filter1d(df_all['HbO_subcu_low'], window_size, mode='nearest')
# df_all['HbR_subcu_low'] = uniform_filter1d(df_all['HbR_subcu_low'], window_size, mode='nearest')
# df_all['HbO_muscle_low'] = uniform_filter1d(df_all['HbO_muscle_low'], window_size, mode='nearest')
# df_all['HbR_muscle_low'] = uniform_filter1d(df_all['HbR_muscle_low'], window_size, mode='nearest')

# df_all['HbO_dermis_up'] = uniform_filter1d(df_all['HbO_dermis_up'], window_size, mode='nearest')
# df_all['HbR_dermis_up'] = uniform_filter1d(df_all['HbR_dermis_up'], window_size, mode='nearest')
# df_all['HbO_subcu_up'] = uniform_filter1d(df_all['HbO_subcu_up'], window_size, mode='nearest')
# df_all['HbR_subcu_up'] = uniform_filter1d(df_all['HbR_subcu_up'], window_size, mode='nearest')
# df_all['HbO_muscle_up'] = uniform_filter1d(df_all['HbO_muscle_up'], window_size, mode='nearest')
# df_all['HbR_muscle_up'] = uniform_filter1d(df_all['HbR_muscle_up'], window_size, mode='nearest')

# df_all['Chb_total'] = uniform_filter1d(df_all['Chb_total'], window_size, mode='nearest')
# df_all['alpha_total'] = uniform_filter1d(df_all['alpha_total'], window_size, mode='nearest')
# drop_index = [i for i in np.arange(0, (window_size-1)//2)] + [i for i in np.arange(df_all.shape[0]-1, df_all.shape[0]-1-(window_size-1)//2, -1)]
# df_all = df_all.drop(drop_index)
# df_all = df_all.reset_index(drop=True)
df_time = df_time.iloc[0:df_all.shape[0], :]
df_all['time'] = df_time['time']
df_all.to_csv(ofilename+'.csv', index=False)

layer = ['dermis', 'subcu.', 'muscle']

df_chb = pd.DataFrame(np.zeros((df_all.shape[0], 6)), columns=['HbO_dermis', 'HbR_dermis', 'HbO_subcu', 'HbR_subcu', 'HbO_muscle', 'HbR_muscle'], index=df_all['time'].values)
df_chb['HbO_dermis'] = df_all['Chb2'].values * df_all['alpha2'].values
df_chb['HbR_dermis'] = df_all['Chb2'].values * (1-df_all['alpha2']).values
df_chb['HbO_subcu'] = df_all['Chb3'].values * df_all['alpha3'].values
df_chb['HbR_subcu'] = df_all['Chb3'].values * (1-df_all['alpha3']).values
df_chb['HbO_muscle'] = df_all['Chb4'].values * df_all['alpha4'].values
df_chb['HbR_muscle'] = df_all['Chb4'].values * (1-df_all['alpha4']).values
df_chb['HbO_dermis'] = df_chb['HbO_dermis']-df_chb.loc[:10, 'HbO_dermis'].mean(axis=0)
df_chb['HbR_dermis'] = df_chb['HbR_dermis']-df_chb.loc[:10, 'HbR_dermis'].mean(axis=0)
df_chb['HbO_subcu'] = df_chb['HbO_subcu']-df_chb.loc[:10, 'HbO_subcu'].mean(axis=0)
df_chb['HbR_subcu'] = df_chb['HbR_subcu']-df_chb.loc[:10, 'HbR_subcu'].mean(axis=0)
df_chb['HbO_muscle'] = df_chb['HbO_muscle']-df_chb.loc[:10, 'HbO_muscle'].mean(axis=0)
df_chb['HbR_muscle'] = df_chb['HbR_muscle']-df_chb.loc[:10, 'HbR_muscle'].mean(axis=0)

# df_all['HbO_dermis_low'] = df_all['HbO_dermis_low']-df_chb.loc[:10, 'HbO_dermis'].mean(axis=0)
# df_all['HbR_dermis_low'] = df_all['HbR_dermis_low']-df_chb.loc[:10, 'HbR_dermis'].mean(axis=0)
# df_all['HbO_subcu_low'] = df_all['HbO_subcu_low']-df_chb.loc[:10, 'HbO_subcu'].mean(axis=0)
# df_all['HbR_subcu_low'] = df_all['HbR_subcu_low']-df_chb.loc[:10, 'HbR_subcu'].mean(axis=0)
# df_all['HbO_muscle_low'] = df_all['HbO_muscle_low']-df_chb.loc[:10, 'HbO_muscle'].mean(axis=0)
# df_all['HbR_muscle_low'] = df_all['HbR_muscle_low']-df_chb.loc[:10, 'HbR_muscle'].mean(axis=0)

# df_all['HbO_dermis_up'] = df_all['HbO_dermis_up']-df_chb.loc[:10, 'HbO_dermis'].mean(axis=0)
# df_all['HbR_dermis_up'] = df_all['HbR_dermis_up']-df_chb.loc[:10, 'HbR_dermis'].mean(axis=0)
# df_all['HbO_subcu_up'] = df_all['HbO_subcu_up']-df_chb.loc[:10, 'HbO_subcu'].mean(axis=0)
# df_all['HbR_subcu_up'] = df_all['HbR_subcu_up']-df_chb.loc[:10, 'HbR_subcu'].mean(axis=0)
# df_all['HbO_muscle_up'] = df_all['HbO_muscle_up']-df_chb.loc[:10, 'HbO_muscle'].mean(axis=0)
# df_all['HbR_muscle_up'] = df_all['HbR_muscle_up']-df_chb.loc[:10, 'HbR_muscle'].mean(axis=0)


df_chb = df_chb[(df_all['RMSP']<=15).to_numpy()]
df_all = df_all[(df_all['RMSP']<=15).to_numpy()]
# df_chb['HbO_dermis'] = uniform_filter1d(df_chb['HbO_dermis'], window_size, mode='nearest')
# df_chb['HbR_dermis'] = uniform_filter1d(df_chb['HbR_dermis'], window_size, mode='nearest')
# df_chb['HbO_subcu'] = uniform_filter1d(df_chb['HbO_subcu'], window_size, mode='nearest')
# df_chb['HbR_subcu'] = uniform_filter1d(df_chb['HbR_subcu'], window_size, mode='nearest')
# df_chb['HbO_muscle'] = uniform_filter1d(df_chb['HbO_muscle'], window_size, mode='nearest')
# df_chb['HbR_muscle'] = uniform_filter1d(df_chb['HbR_muscle'], window_size, mode='nearest')

plt.figure(figsize=(12, 6))
ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
ax2 = plt.subplot2grid((4, 1), (3, 0))
ax1.plot(df_chb.index,df_chb['HbO_dermis'], 'r', marker='o', markerfacecolor='none', label='HbO_dermis')
ax1.plot(df_chb.index,df_chb['HbR_dermis'], 'b', marker='o', markerfacecolor='none', label='HbR_dermis')
ax1.plot(df_chb.index,df_chb['HbO_subcu'], 'r', marker='v', markerfacecolor='none', label='HbO_subcu')
ax1.plot(df_chb.index,df_chb['HbR_subcu'], 'b', marker='v', markerfacecolor='none', label='HbR_subcu')
ax1.plot(df_chb.index,df_chb['HbO_muscle'], 'r', marker='s', markerfacecolor='none', label='HbO_muscle')
ax1.plot(df_chb.index,df_chb['HbR_muscle'], 'b', marker='s', markerfacecolor='none', label='HbR_muscle')
# ax1.errorbar(df_chb.index,df_chb['HbO_dermis'], yerr=[df_all['HbO_dermis_low'], df_all['HbO_dermis_up']])







ax2.plot(df_all['time'], df_all['RMSP'], 'b')
ax2.set_xlabel('Time (secs)')
ax1.set_ylabel('ΔConc. (M)')
ax2.set_ylabel('RMSPE (%)')
ax1.axvspan(xmin=358, xmax=362, color='blue', alpha=0.3)
ax1.axvspan(xmin=58, xmax=62, color='red', alpha=0.3)
ax1.grid(linestyle='--')
ax1.legend(frameon=False, bbox_to_anchor=(1.2, 1))
plt.suptitle(f'{occlusion_type}, {day} subject {subject}')
plt.tight_layout()
plt.savefig(os.path.join(outpath, ofilename+'.png'), dpi=300)
# for i, ly in enumerate(layer):
#     plt.subplot(3, 2, 1+2*i)
#     plt.plot(df_all['time'], df_all['Chb'+str(i+2)])
#     plt.xlabel('Time (secs)')
#     plt.ylabel('Chb')
#     plt.axvspan(xmin=58, xmax=62, color='red', alpha=0.3)
#     plt.axvspan(xmin=358, xmax=362, color='blue', alpha=0.3)
#     plt.grid()
#     plt.subplot(3, 2, 2+2*i)
#     plt.plot(df_all['time'], df_all['alpha'+str(i+2)])
#     plt.xlabel('Time (secs)')
#     plt.ylabel('StO2')
#     plt.axvspan(xmin=58, xmax=62, color='red', alpha=0.3)
#     plt.axvspan(xmin=358, xmax=362, color='blue', alpha=0.3)
#     plt.grid()
#     plt.title(ly)
# plt.suptitle(f'{occlusion_type}, {day} subject {subject}')
# plt.tight_layout()
# plt.savefig(os.path.join(outpath, ofilename+'.png'), dpi=300)
    
# plt.figure()
# plt.subplot(1, 2, 1)
# plt.plot(df_all['time'], df_all['Chb_total'])
# plt.xlabel('Time (secs)')
# plt.ylabel('Chb')
# plt.axvspan(xmin=58, xmax=62, color='red', alpha=0.3)
# plt.axvspan(xmin=358, xmax=362, color='blue', alpha=0.3)
# plt.grid()
# plt.subplot(1, 2, 2)
# plt.plot(df_all['time'], df_all['alpha_total'])
# plt.xlabel('Time (secs)')
# plt.ylabel('StO2')
# plt.axvspan(xmin=58, xmax=62, color='red', alpha=0.3)
# plt.axvspan(xmin=358, xmax=362, color='blue', alpha=0.3)
# plt.grid()
# plt.suptitle(f'total, {occlusion_type}, {day} subject {subject}')
# plt.tight_layout()
# plt.savefig(os.path.join(outpath, ofilename+f'_total.png'), dpi=300)    
    
plt.figure()
plt.plot(df_all['time'], df_all['RMSP'])
plt.xlabel('Time (secs)')
plt.ylabel('RMSPE (%)')
plt.title(f'{occlusion_type}, {day} subject {subject}')
plt.savefig(os.path.join(outpath, ofilename+'_rmsp.png'), dpi=300)