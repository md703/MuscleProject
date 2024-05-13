# %%
import numpy as np
import os
import pandas as pd
import skimage.io 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from glob import glob
from tqdm import tqdm
import process_raw as pr
import matplotlib.ticker as mtick
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# %%
name = 'od1'
folder = 'm_out_20230926/' + name
int_time = np.arange(2, 15, 2, dtype=np.int32)
all_spec = np.zeros((284, int_time.size))
for i, t in enumerate(int_time):
    path = os.path.join(folder, str(t)+'s', 'p6_det_mean.csv')
    df = pd.read_csv(path)
    all_spec[:, i] = df['ch3_mean']
    if i == 0:
        df_wl = df['wl']
df_all_spec = pd.DataFrame(all_spec, columns=['2', '4', '6', '8', '10', '12', '14'])
df_od = pd.concat([df_wl, df_all_spec], axis=1)
df_od.to_csv(os.path.join(folder.split('/')[0], name+'.csv'), index=False)

# %%
folder='m_out_20230926'
int_time = np.arange(2, 15, 2, dtype=np.int32)
x = np.arange(2, 15, 2, dtype=np.int32)
df_od1 = pd.read_csv('m_out_20230926/od1.csv')
df_od04 = pd.read_csv('m_out_20230926/od0.4.csv')
x *= 7551
r2 = r2_score(df_od04.iloc[157, 1:], x)
df_od1_3p98 = df_od1.copy()
df_od1_3p98.iloc[:, 1:]= (df_od1_3p98.iloc[:, 1:]+444.34) * 3.9810717 - 444.34
reg_table_od1 = []
xs = int_time[:, np.newaxis]
for wl in range(df_od1.shape[0]):
    ys = df_od1_3p98.iloc[wl, 1:].values
    ys = ys[:, np.newaxis]
    reg = LinearRegression(fit_intercept=True).fit(xs, ys)
    reg_table_od1.append(reg)
    
reg_table_od4 = []
xs = int_time[:, np.newaxis]
for wl in range(df_od1.shape[0]):
    ys = df_od04.iloc[wl, 1:].values
    ys = ys[:, np.newaxis]
    reg = LinearRegression(fit_intercept=True).fit(xs, ys)
    reg_table_od4.append(reg)
    
rmse_table = np.zeros(df_od1.shape[0])
for wl in range(df_od1.shape[0]):
    y1 = reg_table_od1[wl].predict(xs)
    y4 = reg_table_od4[wl].predict(xs)
    mse = np.sum(np.square((y1-y4)/y4*100)) / y1.size
    rmse = np.sqrt(mse)
    rmse_table[wl] = rmse

df_r2 = pd.concat([df_od1[['wl']], pd.DataFrame(rmse_table)], axis=1)
df_r2.to_csv(os.path.join(folder, 'r2.csv'), index=False)


pass
# %%
folder='m_out_20230926'
int_time = np.arange(2, 15, 2, dtype=np.int32)
x = np.arange(2, 15, 2, dtype=np.int32)
df_od04 = pd.read_csv('m_out_20230926/od0.4.csv')

reg_table = []
r2_table = np.zeros(df_od1.shape[0])
xs = int_time[:, np.newaxis]
for wl in range(df_od1.shape[0]):
    ys = df_od04.iloc[wl, 1:].values
    ys = ys[:, np.newaxis]
    reg = LinearRegression(fit_intercept=False).fit(xs, ys)
    reg_table.append(reg)
    score = reg_table[wl].score(xs, ys)
    r2_table[wl] = score

df_r2 = pd.concat([df_od1[['wl']], pd.DataFrame(r2_table)], axis=1)
df_r2.to_csv(os.path.join(folder, 'r2_wl.csv'), index=False)

# %%
