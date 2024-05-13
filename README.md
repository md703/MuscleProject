Muscle Project
===
-   Author: [Lee, Hao-Wei](https://leeweix.github.io/)
-   License: 
-   Update Date: 2024/5/13
-   Download Size: 128 MB
-   Github Link: https://github.com/leeweix/MuscleProject
-   Contact :email:: kh7227kk@gmail.com 

> [!NOTE] 
> This is the description of the Muscle project, which aims to ensure code behavior consistency. Please ensure that your environment aligns with the following specifications.

![Static Badge](https://img.shields.io/badge/matlab-R2021b-brown)
![Static Badge](https://img.shields.io/badge/python-v3.8.0-blue)
![Static Badge](https://img.shields.io/badge/pip-v20.2.0_(python3.8)-orange)
![Static Badge](https://img.shields.io/badge/cuda-v11.7.0-green)
![Static Badge](https://img.shields.io/badge/OS-ubuntu_18.04_or_win10-purple)



## Table of Contents
- [Muscle Project](#muscle-project)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Overview](#overview)
    - [*In-vivo* measurement](#in-vivo-measurement)
    - [Simulation](#simulation)
    - [Extract optical parameters](#extract-optical-parameters)
  - [Desciprtion of Each Folder](#desciprtion-of-each-folder)
  - [Reference](#reference)

## Introduction
> &nbsp;&nbsp;&nbsp;Quantifying tissue optical parameters facilitates the use of photons for in-vivo diagnosis and treatment. However, the existing literature lacks consideration of optical parameters of superficial tissues when measuring optical parameters of muscle tissue. The goal of this study is to stably measure the optical parameters of neck muscle.  
> &nbsp;&nbsp;&nbsp;The measurement part is a self-built diffuse reflectance spectroscopy system, which uses broadband light-emitting diodes and three-channel self-made optical fibers (SDS=4.5, 7.5, 10.5 mm), and also the analysis wavelength range is 711~880 nm.  
> &nbsp;&nbsp;&nbsp;A Monte Carlo model was established based on the layer thickness of the subject's dermis and subcutaneous fat tissue, and a neural network surrogate model was trained as a forward tool to accelerate simulation. The average root mean square error of the surrogate model was less than 2% . The $\mu_a(\lambda)$ ranges of the epidermis, dermis, subcutaneous fat and muscle layers are 0.18~35, 0.01~2, 0.06~2 and 0.01~1 $cm^{-1}$ respectively; The $\mu_s(\lambda)$ range are set to 90~580, 1~300, 1~250 and 1$~100 $cm^{-1}$. These ranges cover the values previously reported in the literature. In the epidermis layer, the scattering phase function is obtained through finite-difference time domain simulation with g=0.94. The other tissue layers use the Henyey-Greenstein scattering phase function, with g=0.715 in the dermis layer, g=0.9 in the other tissue layers, and the refractive index is set to 1.4. During the fitting process, $\mu_a(\lambda)$ is determined by calculating the concentration of various chromophores in each tissue layer, and $\mu_s(\lambda)$ is determined through the inverse power law. In this study, a nonlinear iterative curve fitting method was used to extract tissue optical parameters.     
> &nbsp;&nbsp;&nbsp;This study measured the neck region of three participants. The $\mu_a(\lambda)$ we extracted for each tissue was consistent with the range of previous literature. However, $\mu_s'(\lambda)$ in the dermis, subcutaneous fat, and muscle layers was much lower than some previous studies, but closer to the results of an \textit{in-vivo} study. To estimate the accuracy of the quantitative optical parameters, the noise measured on our system was added to the test spectra and fitted. The average root mean square errors of $\mu_a(\lambda)$ and $\mu_s'(\lambda)$ are both less than 23\%. This study also conducted arterial and venous occlusion experiments on the subject's forearm, and the changes in light intensity were consistent with expected physiological state changes.
> 
>  &mdash; <cite>[Lee, Hao-Wei][1]</cite>  

[1]: https://leeweix.github.io/

## Installation
> [!TIP]
> Suggestion: create a ${\rm\color{red}{virtual \space environment}}$ and activate it.  
> **How to creaete a virtual environment?**  
> For **Anaconda** user, Read [**this document**](https://hackmd.io/@aMXX54b3ToSm3kTNB_LuWQ/BJ_No2Rkp)

> [!IMPORTANT]
> 1. make sure your local computer has ${\rm\color{red}{cuda \space toolkit}}$
> 2. ${\rm\color{red}{recompile}}$ the MCML source code at [MD703_edit_MCX_src_v2023/src](https://github.com/ShawnSun1031/IJV-Project/tree/main/MD703_edit_MCX_src_v2023/src)
> 3. Install the dependencies: `pip install -r requirements.txt`



## Overview
### *In-vivo* measurement
1. Get individual spectra from *in-vivo* experiment
2. Preprocess raw data
3. Calibration (remove system response)

### Simulation
1. MCML (Monte Carlo) simulation
2. Train surrogate model (to accerlerate the MC simulation)
    > To understand the concept, read this paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5905904/

### Extract optical parameters
1. Fitting *In-vivo* spectra

## Desciprtion of Each Folder
├── Epsilon      
│   &nbsp;&nbsp;&nbsp;&nbsp;└── ...     
├── MBLL     
│   &nbsp;&nbsp;&nbsp;&nbsp;└── ...  
├── Step0_ProcessRawImg   
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step0_1_run.py**  
│   &nbsp;&nbsp;&nbsp;&nbsp;├── README.md...  
│   &nbsp;&nbsp;&nbsp;&nbsp;└── **Step0_2_Phantom**     
│   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; └── ...  
├── Step1-2_GenerateTrainingData   
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step1_param_generator.m**  
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step2_run_wmc.m**     
│   &nbsp;&nbsp;&nbsp;&nbsp;└── README.md...  
├── Step3_ANNTraining   
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step3_ANN_training.m**     
│   &nbsp;&nbsp;&nbsp;&nbsp;└── README.md...  
├── Step4-6_GenerateTargetSpec   
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step4_sim_param_generator.m**  
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step5_sim_spec_generator.m**  
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step6_database_generator.m**     
│   &nbsp;&nbsp;&nbsp;&nbsp;└── README.md...  
├── Step7_Fitting   
│   &nbsp;&nbsp;&nbsp;&nbsp;├── **Step7_autorun.m**     
│   &nbsp;&nbsp;&nbsp;&nbsp;└── README.md...  
└── README.md   
<!-- * MCX_src_modified_by_MD703
    * We modified the source code of MCX (https://github.com/fangq/mcx). Please see [**this file**](https://hackmd.io/@73X8klpNRmSsdgJzudHbgA/SyeF6nI9P#20210409---mcx_corecu-%E4%BF%AE%E6%94%B9) to check what we modified if you're intereseted in. (adjust the source pattern)   -->

> If you excute Step0~7 step by step, you will get the final result (subject's OPs).  
  
> [!IMPORTANT]
> Please read each 'README.md' in each step
* Epsilon
    * Absorption coefficient of chromophore
* MBLL
    * Do MBLL calculation (if you want to see OPs change)
* Step0_ProcessRawImg
    * Process raw data, including preprocessing, calibration.
* Step1-2_GenerateTrainingData
    * Generate training data for building surrogate model
* Step3_ANNTraining
    * train surrogate model
* Step4-6_GenerateTargetSpec
    * Generate target spectra to test performance of inverse method
    * Generate database spectra to solve initial value problem.
* Step7_Fitting
    * Fit subject's spectra to get optical parameters.


## Reference
* To understand more detail, basically this repository is followed by my master thesis. Please check NAS:Data/BOSI Lab/Thesis/R10 to access the full text version.



[def]: #e
