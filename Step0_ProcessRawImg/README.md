Process raw data
===

>This part will process raw data(.tiff) and output spectra to .csv file  
We gonna do:    
1. Get sum of intensity(y-axis) from each channel
2. Subtract background intensity
3. Output spectra intensity(counts)

## Input
- Experiment photos(in-vivo or phantom), e.g. '../20231026_kb/3_X1.tif'

## Output
- Spectra intensity(counts) each photo, e.g. 'm_out_20231026_kb/kb_neck_det_ch1.csv'
- Spectra mean intensity(counts), e.g. 'm_out_20231026_kb/kb_neck_det_mean.csv'
      
## How to run
### Put raw data(from experiment) in current folder
e.g. '../20231026_kb/...'

### Process raw data

```     
python Step0_1_run.py      
```
Please modify default setting, e.g. IO path, experiment type... 



&nbsp;

Phantom calibration
===

>This part will do phantom calibration, and we'll get calibrated spectra    
We gonna do:    
1. Do phantom simulation to get simulated spectra
2. Calculate calibrated phactor by both simulated and measured spectra of phantom
3. Output *in-vivo* calibrated spectra

## Input
- Experiment spectra

## Output
- Calibrated result, including figure, *in-vivo spectra*...
   
## How to run
```
cd Step0_2_Phantom
```
### Simulate phantom spectra(already done)
```
python simulate.py
```

### Phantom calibration
1. Put previous output folder(e.g. 'm_out_20231026_kb') into 'MeasureData'
2. Run 'abs_calibration.py'
```     
python abs_calibration.py      
```
Please modify default setting, e.g. IO path...  

3. output will be in 'AbsCalibration'. Please check if calibration result is OK.

### Acquire *in-vivo* calibrated spectra
```
python output_invivo.py
```
Please modify default setting, e.g. IO path, calibrated phactor path...  
Output spectra will be in 'InvivoReflectance'
