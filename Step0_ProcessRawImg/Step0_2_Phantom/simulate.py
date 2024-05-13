"""
This script run MCML of phantom you choosed, and plot their reflectance
Input: 'mua'.csv, 'musp'.csv
Output: reflectance of each phantom
"""

# %%
import os 
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from tqdm import tqdm
import shutil
import json

# Default setting
DO_SIM = True
DO_WMC = True
RUN_TIMES = 5
NUM_SDS = 3
P_RUN = '3456'
# ifilename = 'phantom1-6'
ofolder = f'sout_2e9_flattop3'
ofolder = os.path.join('PhantomSim', ofolder)
MCML = 'MCML_GPU_APFLAT'
MCML = MCML+'.exe' if os.name == 'nt' else './'+MCML

# df_mua = pd.read_csv(os.path.join('PhantomOPs', f'mod_proc_mua_cm_{ifilename}.csv'))
# df_musp = pd.read_csv(os.path.join('PhantomOPs', f'mod_proc_musp_cm_{ifilename}.csv'))
df_mua = pd.read_csv(os.path.join('PhantomOPs', f'proc_mua_cm_phantom1-6_3.csv'))
df_musp = pd.read_csv(os.path.join('PhantomOPs', f'proc_musp_cm_phantom1-6_3.csv'))

if not os.path.isdir(ofolder):
        os.mkdir(ofolder)
if os.path.isfile(os.path.join('MCML_GPU', 'summary.json')):
    os.remove(os.path.join('MCML_GPU', 'summary.json'))
    
SP_WL = df_mua['wl']
REFRACTIVE_INDEX = 1.4
G = 0


# %% Simulation
if DO_SIM:
    for n in range(RUN_TIMES):
        print(f'Run: {n}:\n')
        dirname = f'run_{n}'
        if not os.path.isdir(os.path.join(ofolder, dirname)):
            os.mkdir(os.path.join(ofolder, dirname))
        else:
            shutil.rmtree(os.path.join(ofolder, dirname), ignore_errors=True)
            os.mkdir(os.path.join(ofolder, dirname))
        for i, pid in enumerate(P_RUN):
            print(f'\tPhantom: {pid}:\n')
            if DO_WMC:
                df_temp = {
                    'mua' : [0] * df_musp.shape[0],
                    'mus' : df_musp[pid].values,
                    'n' : [REFRACTIVE_INDEX] * df_mua.shape[0],
                    'g' : [G] * df_musp.shape[0]
                }
                df_temp = pd.DataFrame(df_temp)
                reflectance_arr = np.zeros((len(SP_WL), NUM_SDS))
                for sim_id in tqdm(range(df_mua.shape[0])):
                    os.chdir('MCML_GPU')
                    df_temp.iloc[[sim_id], :].to_csv(f'input_{pid}.txt', header=None, index=None, sep=' ')
                    for sds in range(NUM_SDS):
                        if os.path.isfile(f'pathlength_SDS_{sds+1}.txt'):
                            os.remove(f'pathlength_SDS_{sds+1}.txt')
                    # cmd = f'MCML_GPU.exe sim_setup.json input_{pid}.txt output_{pid}.txt -R -P'
                    # MCML = 'MCML_GPU.exe' if os.name == 'nt' else './MCML_GPU'
                    
                    cmd = f'{MCML} sim_setup.json input_{pid}.txt output_{pid}.txt -R -P'
                    res = subprocess.check_output(cmd, shell=True)

                    if n == 0 and i == 0 and sim_id == 0:  # First simulation
                        with open('summary.json') as f:
                            summary = json.load(f)
                        photon_weight = summary['each_photon_weight']
                        shutil.copyfile('summary.json', os.path.join(os.path.pardir, ofolder, 'summary.json'))
                    for sds in range(NUM_SDS):
                        df_pl = pd.read_csv(f'pathlength_SDS_{sds+1}.txt', sep='\t', header=None, usecols=np.arange(0, 3))
                        os.remove(f'pathlength_SDS_{sds+1}.txt')
                        df_pl = df_pl[df_pl.columns[:-1]]   # Last column is nan
                        assert df_pl.isnull().any().any() == False, 'There is nan'
                        weight = df_pl[df_pl.columns[0]]
                        pl = df_pl[df_pl.columns[1]]
                        mua = df_mua.loc[[sim_id], pid].values
                        reflectance = np.sum((weight/photon_weight) * np.exp(-pl*mua))
                        reflectance_arr[sim_id, sds] = reflectance
                    os.chdir(os.path.pardir)
                df_reflectance = pd.DataFrame(data=reflectance_arr) 
                df_reflectance.to_csv(os.path.join(ofolder, dirname, f'output_{pid}.txt'), header=None, index=None, sep=' ' )
            else:
                df_temp = {
                    'mua' : df_mua[pid].values,
                    'mus' : df_musp[pid].values,
                    'n' : [REFRACTIVE_INDEX] * df_mua.shape[0],
                    'g' : [G] * df_musp.shape[0]
                }
                df_temp = pd.DataFrame(df_temp)
                for sim_id in tqdm(range(df_mua.shape[0])):
                    os.chdir('MCML_GPU')
                    df_temp.iloc[[sim_id], :].to_csv(f'input_{pid}.txt', header=None, index=None, sep=' ')
                    if os.name == 'nt':
                        cmd = f'MCML_GPU.exe sim_setup.json input_{pid}.txt ..\\{ofolder}\\{dirname}\\output_{pid}.txt'
                        res = subprocess.check_output(cmd, shell=True)
                        os.chdir('..\\')
                    elif os.name == 'posix':
                        cmd = f'./MCML_GPU sim_setup.json input_{pid}.txt output_{pid}.txt'
                        res = subprocess.check_output(cmd, shell=True)
                        os.chdir('../')
                    else:
                        exit(1)     
            
    src = os.path.join('MCML_GPU', 'sim_setup.json')
    dst = os.path.join(ofolder, 'sim_setup.json')
    shutil.copyfile(src, dst)
    os.remove(os.path.join('MCML_GPU', 'summary.json'))
    print('Simulation finished !!!\n')

# %% Output .csv and Plot
# Default setting
DO_NORMALIZE = False
REF_FIBER = 3
SDS_LIST = [4.5, 7.5, 10.5]
FIBER_AREA = [25**2, 52.5**2, 100**2]

fig_spec, ax_spec = plt.subplots(1, NUM_SDS, figsize=(12, 6), dpi=300)
for pid in tqdm(P_RUN):
    spec = []
    for n in range(RUN_TIMES):
        dirname = f'run_{n}'
        spec.append(pd.read_csv(f'{ofolder}/{dirname}/output_{pid}.txt', sep=' ', header=None))
    fig_cv, ax_cv = plt.subplots(1, NUM_SDS, figsize=(12, 6), dpi=300)
    spec_res = np.zeros((len(SP_WL), NUM_SDS))
    for sds in range(NUM_SDS):
        temp_arr = np.zeros((len(SP_WL), RUN_TIMES))
        for i in range(RUN_TIMES):
            temp_arr[:, i] = spec[i][sds]
        spec_res[:, sds] = np.mean(temp_arr, 1)
        
        # Plot reflectance    
        ax_spec[sds].plot(SP_WL, np.mean(temp_arr, 1), )    
        if pid == P_RUN[-1]:        # last time
            ax_spec[sds].set_xticks(np.arange(700, 881, 30))
            ax_spec[sds].set_xlabel('Wavelength [nm]')
            ax_spec[sds].set_ylabel('Reflectance [-]')
            ax_spec[sds].set_title(f'SDS = {SDS_LIST[sds]} [mm]')
            ax_spec[sds].grid(visible=True)
            if sds == NUM_SDS-1:
                labels = [f'Phantom {ph}' for ph in P_RUN]
                ax_spec[sds].legend(labels, loc='upper right', bbox_to_anchor=(1.5, 1.) )
        
        # Plot CV    
        y1 = 100 * np.std(temp_arr, 1) / np.mean(temp_arr, 1)
        ax_cv[sds].plot(SP_WL, y1)
        ax_cv[sds].set_xticks(np.arange(700, 881, 30))
        ax_cv[sds].yaxis.set_major_formatter(mtick.PercentFormatter())
        ax_cv[sds].set_xlabel('Wavelength [nm]')
        ax_cv[sds].set_ylabel('CV [-]')
        ax_cv[sds].set_title(f'SDS = {SDS_LIST[sds]} [mm]')
        ax_cv[sds].grid(visible=True)
        
    # Normalize spectrum if need
    if DO_NORMALIZE:
        spec_res /= FIBER_AREA
        spec_res /= np.mean(spec_res[:, REF_FIBER-1])     # divided sds1 mean 
    df = pd.DataFrame(spec_res, columns=[f'ch{ch+1}' for ch in range(NUM_SDS)])    
    df_wl = pd.DataFrame(SP_WL, columns=['wl'])    
    df = pd.concat([df_wl, df], axis=1)
    df.to_csv(f'{ofolder}/reflectance_{pid}.csv', index=False)
    fig_cv.suptitle(f'Phantom {pid}')
    fig_cv.tight_layout()
    fig_cv.savefig(f'{ofolder}/cv_{pid}.png')
fig_spec.tight_layout()
fig_spec.savefig(f'{ofolder}/reflectance_all.png')
print('Finished plot !!!')
