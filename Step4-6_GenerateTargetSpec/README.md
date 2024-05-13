Generate target spectra
===

>This part will generate target spectra and database 
We gonna do:    
1. Generate random OPs for target spectra and database
2. Do MCML simulation to get target spectra
3. Use ANN surrogate model to produce database

## Input
- None

## Output
- Target spectra and their OPs, e.g. 'epsilon.txt', 'param_XXX.txt', 'simspec_XXX.txt'
- Database, e.g. 'epsilon.txt', 'db_param.mat', 'db.mat'
      
## How to run
### Generate OPs of target spectra and database 
run 'Step4_sim_param_generator.m'

### Simulate target spectra
run 'Step5_sim_spec_generator.m'

### Produce database
run 'Step6_database_generator.m'

Please modify default setting, e.g. IO path...,


  
