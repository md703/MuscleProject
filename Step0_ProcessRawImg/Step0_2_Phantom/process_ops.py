"""
This script process OPs.csv to our interested wavelengths
Input: 'mua'.csv, 'musp'.csv (unit: mm)
Output: 'mua'.csv, 'musp'.csv (unit: cm)
"""

# %%
import os 
import numpy as np
import pandas as pd

# Default setting
# SP_WL = np.array([700, 708, 716, 724, 732, 739, 745, 752, 759, 769, 779, 788, 798, 805, 812, 820, 826, 832, 840, 854, 866, 880])
# SP_WL = np.array([699.8298, 706.2727, 712.7156,	719.1585, 725.6014,	732.0443,
#                 738.4872, 744.9301, 751.373, 757.8159, 764.2588, 770.7017, 
#                 777.1446, 783.5875, 790.0304, 796.4733, 802.9162, 809.3591,
#                 815.802, 822.2449, 828.6878, 835.1307, 841.5736, 848.0165, 
#                 854.4594, 860.9023, 867.3452, 873.7881, 880.231])
# SP_WL = np.arange(700, 881, 2)
SP_WL = np.array([680,682,684,686,688,892,894,896,898,900])
filename = 'phantom1-6'
pname = '123456'
df_mua = pd.read_csv(os.path.join('PhantomOPs', f'mua_in_mm-{filename}.csv'))
df_musp = pd.read_csv(os.path.join('PhantomOPs', f'musp_in_mm-{filename}.csv'))
omua_filename = f'proc_mua_cm_{filename}_3.csv'
omus_filename = f'proc_musp_cm_{filename}_3.csv'

# Transfer unit from mm^-1 to cm^-1
df_mua[[char for char in pname]] *= 10
df_musp[[char for char in pname]] *= 10

mua_arr = np.zeros((len(SP_WL), df_mua.shape[1]))
musp_arr = np.zeros((len(SP_WL), df_musp.shape[1]))
for i, pid in enumerate(pname):
    mua_arr[:, int(pid)] = np.interp(SP_WL, df_mua['wl'], df_mua[pid])
    musp_arr[:, int(pid)] = np.interp(SP_WL, df_musp['wl'], df_musp[pid])
mua_arr[:, 0] = SP_WL
musp_arr[:, 0] = SP_WL
df_mua_n = pd.DataFrame(mua_arr, columns=['wl']+list(pname))
df_musp_n = pd.DataFrame(musp_arr, columns=['wl']+list(pname))
df_mua_n.to_csv(os.path.join('PhantomOPs', omua_filename), index=False)
df_musp_n.to_csv(os.path.join('PhantomOPs', omus_filename), index=False)