Generate training data
===

>This part will generate training data for surrogate model   
We gonna do:    
1. Generate optical parameters within bound
2. Do MCML simulation with each OPs

## Input
- None

## Output
- OPs which we generated, e.g. '2023_0731_thick9.txt'
- Simulated spectra, e.g. 'spec_1to875.mat'
      
## How to run
### Generate optical parameters
run 'Step1_param_generator.m'

### Do MCML simulation

run 'Step2_run_wmc.m'   
