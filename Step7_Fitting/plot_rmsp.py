import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
from glob import glob
from natsort import natsorted
from tqdm import tqdm

subject = ['eu', 'kb', 'by']
pathlist = ['eu_neck1016_dilated_db20w_sp72319', 'kb_neck1026_dilated_db20w', 'by_neck1102_dilated_db20w_sp72319']
title = ['eu 1016', 'kb 1026', 'by 1102']
font = 13

for i, path in tqdm(enumerate(pathlist)):
    path2 = glob(os.path.join(path, '*'))
    df = pd.read_csv(os.path.join(path2[0], 'fit_res.csv'))
    plt.figure()
    plt.scatter(df.index.values+1, df['RMSP'].sort_values(), color='b', marker='o', facecolors='none') 
    plt.ylim(top=100, bottom=0)
    plt.xticks(np.arange(1, 21))
    plt.axhspan(0, np.min(df['RMSP']) + 1, facecolor ='r', alpha = 0.2)
    plt.ylabel('RMSPE (%)', fontsize=font)
    plt.xlabel('Index', fontsize=font)
    plt.grid(linestyle='--')
    plt.title(title[i], fontsize=font+1)
    plt.tight_layout()
    plt.savefig(os.path.join(path2[0], f'{subject[i]}_neck_rmsp.png'), dpi=300)
    pass