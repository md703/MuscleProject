% Use ANN to fitting
% Tzu-Chia Kao 20181027
% Hao-Wei Lee 20221115

% target_spec: the path to target
function result_arr=fitting(target_spec, x0_arr, OUTPUT_FOLDER, target_name)
    global RECORD_EACH_FIT; RECORD_EACH_FIT=0;          % =1, output lsqMu......
    global do_MC_sim;                                   % =1, run MCML simulation after fitting   
    global sds_choose net OUTPUT_FOLDER_L2 lambda 
    global mu_epi mu_mel epsilon_oxy epsilon_deoxy mu_water mu_collagen mu_lipid
    global fid_epi fid_mel fid_hemo fid_water fid_collagen fid_lipid thick fitThickness wl_all

    % interp fitting wavelength
%     mu_epi = interp1(fid_epi(:, 1), fid_epi(:, 2), lambda(:,1));
%     mu_mel = interp1(fid_mel(:, 1), fid_mel(:, 2), lambda(:,1));
%     epsilon_oxy = interp1(fid_hemo(:, 1), fid_hemo(:, 2), lambda(:,1));
%     epsilon_deoxy = interp1(fid_hemo(:, 1), fid_hemo(:, 3), lambda(:,1));
%     mu_water = interp1(fid_water(:, 1), fid_water(:, 2), lambda(:,1));
%     mu_collagen = interp1(fid_collagen(:, 1), fid_collagen(:, 2), lambda(:,1));
%     mu_lipid = interp1(fid_lipid(:, 1), fid_lipid(:, 2), lambda(:,1));   
    
    wl_all = 650:910;
    wl_all = wl_all';
    mu_epi = interp1(fid_epi(:, 1), fid_epi(:, 2), wl_all);
    mu_mel = interp1(fid_mel(:, 1), fid_mel(:, 2), wl_all);
    epsilon_oxy = interp1(fid_hemo(:, 1), fid_hemo(:, 2), wl_all);
    epsilon_deoxy = interp1(fid_hemo(:, 1), fid_hemo(:, 3), wl_all);
    mu_water = interp1(fid_water(:, 1), fid_water(:, 2), wl_all, 'linear', 'extrap');
    mu_collagen = interp1(fid_collagen(:, 1), fid_collagen(:, 2), wl_all);
    mu_lipid = interp1(fid_lipid(:, 1), fid_lipid(:, 2), wl_all);

    num_fitting=size(x0_arr,1);

    if do_MC_sim==1 
        if fitThickness==1
            result_arr=zeros(size(x0_arr,1),size(x0_arr,2)+2); 
        else
            result_arr=zeros(size(x0_arr,1),size(x0_arr,2)+5); 
        end
    else
        if fitThickness==1
            result_arr=zeros(size(x0_arr,1),size(x0_arr,2)+1);
        else
            result_arr=zeros(size(x0_arr,1),size(x0_arr,2)+4);
        end
    end
    
    %% ############ Fitting each initial value ############
    for fitting_counter=1:num_fitting
        global conuter_lsqcurfit; conuter_lsqcurfit = 1;
        global RUNFINALSPEC; RUNFINALSPEC = 1;              % 1:using final fitting result to generate spectra; 0: don't     
        global final; final=0;                              % not output final spec yet
        global fitID; fitID = fitting_counter;
        global spec_target spec_target_raw; 
        global Lbound Ubound varName folder_index spec_id
        OUTPUT_FOLDER_L2 = fullfile(OUTPUT_FOLDER, ['fit_all' num2str(fitting_counter)]);  
        if (exist(OUTPUT_FOLDER,'dir')==7)
            mkdir(OUTPUT_FOLDER_L2);            
        else 
            mkdir(OUTPUT_FOLDER);
            mkdir(OUTPUT_FOLDER_L2);  
        end % clear previous result from folder 'output' 
        
%         lb = [0.01  0.049  0.276  90     140    80     20     0.18   0.01   0.06   0.01 ];
%         ub = [0.01  0.049  0.276  580    330    270    100    35     2      2      1 ];
        %  ######################## Param bound ########################
        if folder_index == 1 || folder_index == 2
%             thick = [0.01	0.276243	0.359116];
            thick = [0.01 0.18599 0.07488];
        elseif folder_index == 3 || folder_index == 4
            thick = [0.01	0.1380368	0.15030674];
        elseif folder_index == 5 || folder_index == 6
            thick = [0.01	0.16895604	0.225274725];
        end
%         thick = [0.01 0.169 0.225];
        varName = {'th1' 'th2' 'th3' 'fmel'     'Chb2' 'alpha2' 'Chb3'  'alpha3' 'Chb4' 'alpha4' 'A1'       'k1'   'A2'       'k2'     'A3'    'k3'    'A4'   'k4' 'fcol2' 'flipid3' 'flipid4'};
        
        %         1026 kb forearm
%         Lbound =  [0.01   1.6895604e-01    2.25274725e-01     0.001    0.12     0     0.12      0        0.12     0       10      0.58    0.78       0.24      1.8    0.68      4    0.61    0       0        0]; % lower boundary
%         Ubound =  [0.01   1.6895604e-01    2.25274725e-01     0.16     4.8      1     4.8       1        4.8      1       2662    1.41    10897      1.63      48     0.88    940    1.51    1       1        1]; % upper boundary
%         Lbound =  [     0.001    0.12     0     0.12      0        0.12     0       10      0.1    0.78       0.1      1.8    0.1      4    0.1    0       0        0]; % lower boundary
%         Ubound =  [     0.16     4.8      1     4.8       1        4.8      1       2662    5    10897      5      48     5    940    5    1       1        1]; % upper boundary
        
%         change chb range
%         Lbound =  [     0.001    0.12     0.5     0.12      0.5        0.12     0.5       10      0.1    0.78      0.1    1.8    0.1    4    0.1    0.5       0.001        0.5]; % lower boundary
%         Ubound =  [     0.4     5         1       2         1             5       1      2662    2     10897      2      48     2    940    2      0.5       0.001        0.5]; % upper boundary
%         Lbound =  [     0        0       0     0        0        0       0       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0       0        0]; % lower boundary
%         Ubound =  [     0.16     20      1     20       1        20      1       2662    5    10897      5      48     5    940    5      2       2        2]; % upper boundary
%         Lbound =  [     0        0.000001 0 0.000001 0 0.000001 0       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0       0        0]; % lower boundary
%         Ubound =  [     0.16     0.00015  1 0.00015  1 0.00015  1       2662    5    10897      5      48     5    940    5      2       2        2]; % upper boundary
%         Lbound =  [     0        0.12    0  0.12  0 0.12   0       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0       0        0]; % lower boundary
%         Ubound =  [     0.16     60      1  60    1 60     1       2662    5    10897      5      48     5    940    5      1       1        1]; % upper boundary
%         Lbound =  [     0        0.12    0  0.12  0 0.12   0       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0.5       0.01        0.5]; % lower boundary
%         Ubound =  [     0.16     60      1  60    1 60     1       2662    5    10897      5      48     5    940    5      0.5       0.01        0.5]; % upper boundary
%         Lbound =  [     0        0.12    0.5  0.12  0.5 0.12   0.5       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0.5       0.01        0.5]; % lower boundary
%         Ubound =  [     0.16     60      0.8  60    0.8 60     0.8       2662    5    10897      5      48     5    940    5      0.5       0.01        0.5]; % upper boundary
        
        Lbound =  [     0.0001   0   0.5  0    0.5  0   0.5    10     0    10     0    10      0     10      0      0     0      0]; % lower boundary
        Ubound =  [     0.2     60   1   60    1   60   1    1000     2    175    2   250    2    1000     2      10     2     10]; % upper boundary
%         Lbound =  [     0        0.12    0.5  0.12  0.5 0.12   0.5       0      0    0      0    0     0    0     0    0.5       0.001        0.5]; % lower boundary
%         Ubound =  [     0.16     60      0.8  60    0.8 60     0.8       1000   2    1000   2    1000  2    1000  2    0.5       0.01        0.5]; % upper boundary
%         Lbound =  [     0        0.12    0.5  0.12  0.5 0.12   0.5       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0.5       0.001        0.5]; % lower boundary
%         Ubound =  [     0.16     60      0.8  60    0.8 60     0.8       2662    5    10897      5      48     5    940    5      0.5       0.01        0.5]; % upper boundary
%         Lbound =  [     0        0.12    0  0.12  0 0.12   0       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0.5       0.001        0.5]; % lower boundary
%         Ubound =  [     0.16     60      1  60    1 60     1       2662    5    10897      5      48     5    940    5      0.5       0.01        0.5]; % upper boundary
%         Lbound =  [     0        0.12    0.5  0.12  0.5 0.12   0.5       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0       0        0]; % lower boundary
%         Ubound =  [     0.16     60      0.8  60    0.8 60     0.8       2662    5    10897      5      48     5    940    5      1       1        1]; % upper boundary
%         if folder_index == 1
%     %       1006 syu arterial
% %             Lbound = [0.143595	10.391	0 16.4951  0	19.9596	 0  1506.5025	1.43445	4495.3115	1.877872	17.375437	0.725404	715.16931	1.608625	2	0.001015	1.999992];
% %             Ubound = [0.143595	10.433  1 16.5612  1    20.0396  1	1506.5025	1.43445	4495.3115	1.877872	17.375437	0.725404	715.16931	1.608625	2	0.001015	1.999992];
% %               Lbound =  [     0        0.12    0.5  0.12  0.5 0.12   0.5       10      0.1    0.78     0.1    1.8    0.1    4    0.1    0.5       0.01        0.5]; % lower boundary
% %               Ubound =  [     0.16     60      0.8  60    0.8 60     0.8       2662    5    10897      5      48     5    940    5      0.5       0.01        0.5]; % upper boundary
%               if spec_id<=20
%                   Lbound = [0.096176	0.95*9.876073	0.5	0.95*18.420811	0.5	0.95*14.480661	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.096176	1.05*9.876073	0.8	1.05*18.420811	0.8	1.05*14.480661	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];
%               elseif spec_id>20 && spec_id<=160
%                   Lbound = [0.152778 0.5*6.983973	0	0.5*19.750223	0	0.5*9.308653	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.152778 1.5*6.983973	1	1.5*19.750223	1	1.5*9.308653	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>160
%                   Lbound = [0.143203	0.95*9.725758	0.5	0.95*18.232574	0.5	0.95*15.516833	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.143203	1.05*9.725758	0.8	1.05*18.232574	0.8	1.05*15.516833	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         elseif folder_index == 2
%     %       1006 syu venous
% %             Lbound = [0.005102	0	0	0	0	0	0	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634];
% %             Ubound = [0.005102	20	1	20	1	20	1	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634];        
% %             Lbound = [0.005102	7.7606	0   7.5182	0	19.9586	 0  1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634];
% %             Ubound = [0.005102	7.7918  1   7.5484  1   20.0386  1	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634];        
%              if spec_id<=20
%                   Lbound = [0.013879	0.95*9.025496	0.5	0.95*6.364691	0.5	0.95*6.585391	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.013879	1.05*9.025496	0.8	1.05*6.364691	0.8	1.05*6.585391	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];
%               elseif spec_id>20 && spec_id<=129
%                   Lbound = [0.011016 0.5*14.113763	0	0.5*15.999809	0	0.5*2.113134	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.011016 1.5*14.113763	1	1.5*15.999809	1	1.5*2.113134	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>129
%                   Lbound = [0.013308	0.95*7.169453	0.5	0.95*6.158249	0.5	0.95*9.679013	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.013308	1.05*7.169453	0.8	1.05*6.158249	0.8	1.05*9.679013	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         elseif folder_index == 3
%     %       1016 eu arterial
% %           Lbound =  [     0.038296    0     0     0      0        0     0       1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]; % lower boundary
% %           Ubound =  [     0.038296   20     1    20      1       20     1       1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]; % upper boundary
% %           Lbound =  [     0.038296   3.1166	 0	18.8539	 0	11.04    0  1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]; % lower boundary
% %           Ubound =  [     0.038296   3.1291  1  18.9295  1  11.0842  1  1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]; % upper boundary
%             if spec_id<=20
%                   Lbound = [0.065014	0.95*11.09476	0.5	0.95*3.348782	0.5	0.95*11.952731	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.065014	1.05*11.09476	0.8	1.05*3.348782	0.8	1.05*11.952731	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];       
%               elseif spec_id>20 && spec_id<=160
%                   Lbound = [0.04658 0.5*8.467423	0	0.5*13.089044	0	0.5*14.090072	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.04658 1.5*8.467423	1	1.5*13.089044	1	1.5*14.090072	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>160
%                   Lbound = [0.065084	0.95*10.428203	0.5	0.95*10.957918	0.5	0.95*7.816072	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.065084	1.05*10.428203	0.8	1.05*10.957918	0.8	1.05*7.816072	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         elseif folder_index == 4
%     %       1016 eu venous
% %           Lbound = [0.09158	0     0     0      0        0     0	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603];
% %           Ubound = [0.09158	20     1    20      1       20     1	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603];
% %           Lbound = [0.09158	19.96  0 11.7957  0	0.1879	0 	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603];
% %           Ubound = [0.09158	20.04  1 11.8430  1 0.1887  1	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603];
%             if spec_id<=20
%                   Lbound = [0.084952	0.95*23.774446	0.5	0.95*9.822715	0.5	0.95*0.599737	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.084952	1.05*23.774446	0.8	1.05*9.822715	0.8	1.05*0.599737	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];
%               elseif spec_id>20 && spec_id<=129
%                   Lbound = [0.09158 0.5*18.652214	0	0.5*16.941143	0	0.5*1.040183	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.09158 1.5*18.652214	1	1.5*16.941143	1	1.5*1.040183	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>129
%                   Lbound = [0.107349	0.95*14.30959	0.5	0.95*13.549936	0.5	0.95*1.039486	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.107349	1.05*14.30959	0.8	1.05*13.549936	0.8	1.05*1.039486	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         elseif folder_index == 5
%     %       1026 kb arterial
% %             Lbound = [0.16	15.1743	 0 20.04  0	20.04  0	1657.428711	1.214723	4147.046875	1.907901	15.211372	0.964941	671.77063	1.345197	2	3.90E-05	1.999997];
% %             Ubound = [0.16	15.2352  1 19.96  1 19.96  1	1657.428711	1.214723	4147.046875	1.907901	15.211372	0.964941	671.77063	1.345197	2	3.90E-05	1.999997];
%             if spec_id<=20
%                   Lbound = [0.138943	0.95*19.810436	0.5	0.95*18.932894	0.5	0.95*18.748545	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.138943	1.05*19.810436	0.8	1.05*18.932894	0.8	1.05*18.748545	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];
%               elseif spec_id>20 && spec_id<=160
%                   Lbound = [0.147861 0.5*18.145227	0	0.5*17.40707	0	0.5*25.354588	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.147861 1.5*18.145227	1	1.5*17.40707	1	1.5*25.354588	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>160
%                   Lbound = [0.149633	0.95*14.170774	0.5	0.95*23.89538	0.5	0.95*17.269381	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.149633	1.05*14.170774	0.8	1.05*23.89538	0.8	1.05*17.269381	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         elseif folder_index == 6
%     %       1026 kb venous
% %             Lbound = [0.16	0	0	0	0	0	0	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';
% %             Ubound = [0.16	20	1	20	1	20	1	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';
% %             Lbound = [0.16	11.7673	 0	20.04  0 20.04	0   1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';
% %             Ubound = [0.16	11.8145  1  19.96  1 19.96  1	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';
%             if spec_id<=20
%                   Lbound = [0.1555	0.95*18.333693	0.5	0.95*14.047987	0.5	0.95*18.766418	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.1555	1.05*18.333693	0.8	1.05*14.047987	0.8	1.05*18.766418	0.8	2662    5    10897      5      48     5    940    5	   0.5	0.01	0.5];
%               elseif spec_id>20 && spec_id<=129
%                   Lbound = [0.155751 0.5*17.434731	0	0.5*22.421045	0	0.5*18.952002	0   10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.155751 1.5*17.434731	1	1.5*22.421045	1	1.5*18.952002	1	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               elseif spec_id>129
%                   Lbound = [0.119291	0.95*13.833104	0.5	0.95*29.727032	0.5	0.95*18.379358	0.5	10      0.1    0.78     0.1    1.8    0.1    4    0.1	0.5	0.01	0.5];
%                   Ubound = [0.119291	1.05*13.833104	0.8	1.05*29.727032	0.8	1.05*18.379358	0.8	2662    5    10897      5      48     5    940    5	    0.5	0.01	0.5];
%               end
%         end
        if fitThickness == true
            thick = x0_arr(fitting_counter,1:3);
            x0 = x0_arr(fitting_counter,4:end);
        else
            x0 = x0_arr(fitting_counter,:);
        end
%         if fitting_counter==num_fitting
%             if folder_index == 1
%                 x0 = [0.143595	10.412265	0.999989	16.528183	0.328206	19.999619	0.365613	1506.502563	1.43445	4495.311523	1.877872	17.375437	0.725404	715.169312	1.608625	2	0.001015	1.999992];
%             elseif folder_index == 2
%                 x0 = [0.005102	7.776186	0.612342	7.53331	0.984396	19.998627	0.954053	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634];
%             elseif folder_index == 3
%                 x0 = [0.038296	3.122947	0.998084	18.891708	0.107828	11.062102	0.993835	1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634];
%             elseif folder_index == 4
%                 x0 = [0.09158	19.999971	0.221542	11.819396	0.99999	0.18834	0.978894	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603];
%             elseif folder_index == 5    
%                 x0 = [0.16	15.204819	0.999987	19.999989	0.667348	19.999956	0.619153	1657.428711	1.214723	4147.046875	1.907901	15.211372	0.964941	671.77063	1.345197	2	3.90E-05	1.999997];
%             elseif folder_index == 6
%                 x0 = [0.16	11.790928	0.999997	19.999966	0.732238	19.999844	0.544568	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993];
%             end
%         end

%         annLb = [        90     10    10     10     0.18   0.01   0.06   0.01 ];
%         annUb = [       580    150    150    100    35     2      2      1 ];
%         annLb = [        10     10    10     10     0.18   0.01   0.06   0.01 ];
%         annUb = [       580    150    150    100    35     2      2      1 ];
        annLb = [        90     10    10     1     0.18   0.01   0.06   0.01 ];
        annUb = [       580    300    300    100    35     2      2      1 ];
%         annLb = [        90    10   10    10    0.18   0.01   0.06   0.01 ];
%         annUb = [       580    300   300    100    35     2      2      1 ];
        %  ########################   Fitting   ########################
        
        
        % options =optimoptions(@fmincon,'Display','iter','StepTolerance',10^-7,'FiniteDifferenceStepSize',stepsize);%original
%         fout = @(x)gaoutfun(x, Lbound, Ubound, varName, OUTPUT_FOLDER_L2);
%         options = optimoptions('ga','OutputFcn', @gaoutfun);
%         options = optimoptions('ga');
        options = optimoptions('fmincon','Algorithm','sqp','Display','iter','DiffMinChange',5*10^-5,'OptimalityTolerance',1e-9,'ConstraintTolerance',1e-12,'StepTolerance',1e-12,'MaxFunctionEvaluations',round(100*length(x0)*1.5)); % increase the min step size for finding gradients

        options.Display = 'iter';
%         options.Algorithm = 'sqp';
%         options.UseParallel = false;
%         options.MaxTime = 1;
%         options.MaxFunEvals = 40000;
%         options.MaxIterations = 10000;
%         options.MaxGenerations = 200*19;
%         options.UseParallel = true;
%         options.StepTolerance = 10^-7;
%         options.FiniteDifferenceStepSize = stepsize;
        fitRoute = fopen('fitRoute.txt', 'w'); fclose(fitRoute); %clear before wrote % before lsqcurvefit
        tic
        time1 = toc;
%         x0(:, [9 11 13 15]) = x0(:, [9 11 13 15])./10000; 
%         [x, fval, exitflag, output] = fmincon(@fun_MC_two_layer, x0, [], [], [], [], Lbound, Ubound, @constraint_4_1, options);
        rng default
        paramcell = {spec_target, conuter_lsqcurfit, sds_choose, lambda, final, RECORD_EACH_FIT,...
                    do_MC_sim, fitID, net, OUTPUT_FOLDER_L2, mu_epi mu_mel epsilon_oxy epsilon_deoxy mu_water mu_collagen mu_lipid};
        f = @(x)fun_MC_two_layer(x, paramcell);
        fcon = @(x)constraint_4_1(x, annUb, annLb, lambda, paramcell(11:17));
%         [x, fval, exitflag, output] = ga(f, 18, [], [], [], [], Lbound, Ubound, fcon, options);
%         [x, fval, exitflag, output] = fmincon(f, x0, [], [], [], [], Lbound, Ubound, fcon, options);
        [x, fval, exitflag, output] = fmincon(f, x0, [], [], [], [], Lbound, Ubound, [], options);
%         [x, fval, exitflag, output] = fmincon(f, x0, [], [], [], [], [], [], [], options);
%         [x, fval, exitflag, output] = ga(f,18,[],[],[],[],Lbound,Ubound,fcon)
        time2 = toc;
        fprintf('    Cost %5.2f seconds.', time2 - time1);
        disp('    ...Done!');
        writestruct(output, fullfile(OUTPUT_FOLDER_L2, 'lsqMSG.xml'));
        %  #############################################################

        % final fitting result, run final spectra
        if (RUNFINALSPEC)
            paramcell{5} = 1; % final = 1;
            fun_MC_two_layer(x, paramcell);
        end
        fitRoute_content=load('fitRoute.txt');
        if do_MC_sim == 1
            result_arr(fitting_counter,:) = [fitRoute_content(end,:) fitRoute_content(end-1,end) ];
        else
            result_arr(fitting_counter,:) = fitRoute_content(end,:);
        end
        dataname = fullfile(OUTPUT_FOLDER_L2, 'lsqSpec_target.txt'); % save target spectra
        save(dataname,'spec_target_raw','-ascii');
        clear fitRoute_content;
        try
            movefile('fitRoute.txt',fullfile(OUTPUT_FOLDER_L2, 'fitRoute.txt'), 'f');
        catch exception
            disp('Can''t move fitRoute.txt')
        end
        movefile(fullfile(OUTPUT_FOLDER_L2, 'fitted_result.png'), fullfile(OUTPUT_FOLDER, 'spec_pics', ['fit_all' num2str(fitting_counter) '.png'])); % copy the result picture to the same folder
        
    end
end

function [c, ceq] = constraint_4_1(para, ub, lb, lambda, epicell)
    global  thick
    [mu] = Mu_generator(para, lambda, epicell);
    th1 = thick(1);
    th2 = thick(2);
    th3 = thick(3);
    mus1 = mu(:,1); 
    mus2 = mu(:,2); 
    mus3 = mu(:,3); 
    mus4 = mu(:,4);
    mua1 = mu(:,5); 
    mua2 = mu(:,6); 
    mua3 = mu(:,7); 
    mua4 = mu(:,8);
    
    % test param in ANN range
    %     {'th1' 'th2' 'th3' 'mus1' 'mus2' 'mus3' 'mus4' 'mua1' 'mua2' 'mua3' 'mua4' }
%     lb = [0.01  0.049  0.276  90     140    80     20     0.18   0.01   0.06   0.01 ];
%     ub = [0.01  0.049  0.276  580    330    270    100    35     2      2      1 ];

    ceq = [];
    c = [mus1 - ub(1);
        mus2 - ub(2);
        mus3 - ub(3);
        mus4 - ub(4);
        lb(1) - mus1;
        lb(2) - mus2;
        lb(3) - mus3;
        lb(4) - mus4;
        mua1 - ub(5);
        mua2 - ub(6);
        mua3 - ub(7);
        mua4 - ub(8);
        lb(5) - mua1;
        lb(6) - mua2;
        lb(7) - mua3;
        lb(8) - mua4;];
end

% when final==1, output file named _final.txt
function MC_weight= fun_MC_two_layer(x0, paramcell)
    global conuter_lsqcurfit spec_target_raw varName  thick fitThickness wl_all
    spec_target = paramcell{1}; 
    sds_choose = paramcell{3};
    lambda = paramcell{4};
    final = paramcell{5};
    RECORD_EACH_FIT = paramcell{6}; % =1, output lsqMu......
    do_MC_sim = paramcell{7}; % =1, run MCML simulation after fitting
    fitID = paramcell{8};
    net = paramcell{9};
    OUTPUT_FOLDER_L2 = paramcell{10};

    actual_para = x0;
    [mu] = Mu_generator(actual_para, wl_all, paramcell(11:17));
%     paramSet = [mu(:, 1) mu(:, 2) mu(:, 3) mu(:, 4) mu(:, 5) mu(:, 6) mu(:, 7) mu(:, 8)];
    spec = ANN_predict_matlab(mu, sds_choose, net); % use ANN to predict spectrum
    spec = spec(:, sds_choose);
    for s=1:size(spec, 2)
%         figure();
        x_axis=-20:1:20;
%         conv_kernal = customSinc(x_axis);
        conv_kernal=normpdf(x_axis,0,3.88/2.355);
        conv_kernal=conv_kernal/sum(conv_kernal);
        conv_kernal = conv_kernal';
%         plot(x_axis,conv_kernal);
%         grid on;
%         hold on;
%         xline(spectralRes(s)/2);
%         xline(-spectralRes(s)/2);
%         yline(max(conv_kernal)/2);
%         xxticks=xticks();
%         xxticks=sort([xxticks spectralRes(s)/2 -spectralRes(s)/2]);
        % xticks(xxticks);
%         xlabel('wavelength(nm)');
%         print(fullfile(output_dir,[num2str(s) '_kernal_discrete.png']),'-dpng','-r200');
        
%         close all;
%         nexttile();
        spec(:,s)=conv(spec(:,s),conv_kernal,'same');
%         plot(orig_spec(:,1),[orig_spec(:,s+1) dilated_spec(:,s+1)]);
%         grid on;
%         legend(legend_arr,'Location','northwest');
%         title(['SDS ' num2str(s)]);
%         ylabel('reflectance');
%         xlabel('wavelength(nm)');
%         set(gca,'fontsize',fontSize, 'FontName', 'Times New Roman');
    end
    spec_temp = zeros(size(lambda, 1), size(spec, 2));
    for s = 1:size(spec, 2)
        spec_temp(:, s) = interp1(wl_all, spec(:, s), lambda);
    end
    spec = spec_temp;
    % RMSP
    de = (spec-spec_target)./spec_target;
    de2 = de.^2;
%     de2(8:10, :) = de2(8:10, :)*100;
    rmsp = sqrt(mean(mean(de2)))*100;
    MC_weight = double(rmsp);
%     fprintf('conuter_lsqcurfit = %d, rmsp = %2.4f%%\n', conuter_lsqcurfit, rmsp);
    
%     if ~final progressbar(conuter_lsqcurfit, parameter_set(end)); end
    
    % run final MC simulation
    if final==1 && do_MC_sim==1
        
        cd data/
        disp('Run final MC');
        % creat MCML input
        g_arr = [-2 0.715 0.9 0.93];
        tissue_n=ones(size(lambda))*1.4;
        g1 = repmat(g_arr(1), size(lambda));
        g2 = repmat(g_arr(2), size(lambda));
        g3 = repmat(g_arr(3), size(lambda));
        g4 = repmat(g_arr(4), size(lambda));
        th1 = repmat(thick(1), size(lambda));
        th2 = repmat(thick(2), size(lambda));
        th3 = repmat(thick(3), size(lambda));
        mus1 = mu(:,1); 
        mus2 = mu(:,2); 
        mus3 = mu(:,3); 
        mus4 = mu(:,4);
        mua1 = mu(:,5); 
        mua2 = mu(:,6); 
        mua3 = mu(:,7); 
        mua4 = mu(:,8);
        MCML_input=[th1 mua1 mus1 tissue_n g1 th2 mua2 mus2 tissue_n g2 th3 mua3 mus3 tissue_n g3 mua4 mus4 tissue_n g4];
        gpuout = fopen('GPUMC_output.txt', 'w'); fclose(gpuout);
        for wl = 1:size(lambda, 1)
            mcinput = MCML_input(wl, :);
            save('GPUMC_input.txt','mcinput','-ascii','-tabs');
            if isunix
                [ret,sta]=system('./MCML_GPU_AP sim_setup.json GPUMC_input.txt GPUMC_output.txt');
            else
                [ret,sta]=system('MCML_GPU_AP.exe sim_setup.json GPUMC_input.txt GPUMC_output.txt');
            end
        end
        cd ../
        MC_spec=load('data/GPUMC_output.txt'); % load MCML output
        dataname = fullfile(OUTPUT_FOLDER_L2, 'lsqMC_final.txt');% save spectra
        save(dataname,'MC_spec','-ascii');
        rw=length(MC_spec)-length(lambda);
        % RMSP
        sds_mcml=[1 2 3];
        de = (MC_spec(1:end-rw, sds_mcml(sds_choose))-spec_target) ./ spec_target;          
        de2 = de.^2;
        rmsp_mc = sqrt(mean(mean(de2)))*100;

        % fitRoute
        fitRoute = fopen('fitRoute.txt', 'a');
        parameter_set = [actual_para rmsp_mc];
        varstr = repmat('%f\t', 1, size(actual_para, 2)+1);
        outstr = strcat('\r\n', varstr);
        fprintf(fitRoute, outstr, parameter_set);
        fclose(fitRoute);
    end
    
    % Save spec, para 
    if final==0
        if RECORD_EACH_FIT==1
            dataname = [ 'output_/' 'lsqSpec_' num2str(conuter_lsqcurfit) '.txt'];% save spectra
            save(dataname,'spec','-ascii');
            dataname = [ 'output_/' 'lsqPara_' num2str(conuter_lsqcurfit) '.txt'];% save parameter
            save(dataname,'parameter_set','-ascii');
            dataname = [ 'output_/' 'lsqMu_' num2str(conuter_lsqcurfit) '.txt'];% save mu
            save(dataname,'mu','-ascii');
        end

        conuter_lsqcurfit = conuter_lsqcurfit + 1;
    elseif final==1
        [mu] = Mu_generator(actual_para, lambda, paramcell(11:17));
        varNames = varName;
        varNames{end+1} = 'RMSP';
        t1 = repmat(thick(1), size(lambda));
        t2 = repmat(thick(2), size(lambda));
        t3 = repmat(thick(3), size(lambda));
        if fitThickness
            mu_set = [lambda  t1 t2 t3 mu(:, 4)  mu(:, 5)  mu(:, 6)  mu(:, 7) mu(:, 8) mu(:, 9) mu(:, 10) mu(:, 11)];
        else
            mu_set = [lambda  t1 t2 t3 mu(:, 1)  mu(:, 2)  mu(:, 3)  mu(:, 4) mu(:, 5) mu(:, 6) mu(:, 7) mu(:, 8)];
        end
%         varNames = {'th1' 'th2' 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'fcol4' 'RMSP'};
        varNames2 = {'wl', 'th1', 'th2', 'th3', 'mus1', 'mus2', 'mus3', 'mus4', 'mua1', 'mua2', 'mua3', 'mua4'};        


        % fitRoute
        fitRoute = fopen('fitRoute.txt', 'a');
        while fitRoute == -1 % if open fail, retry
            fitRoute = fopen('fitRoute.txt', 'a');
        end
        parameter_set = [thick(1) thick(2) thick(3) actual_para rmsp]; 
        varstr = repmat('%f\t', 1, size(parameter_set, 2));
        outstr = strcat('\r\n', varstr);
        fprintf(fitRoute, outstr, parameter_set); fclose(fitRoute);
        

        % Convert single to double
        spec = double(spec);
        parameter_set = double(parameter_set);
        dataname = fullfile(OUTPUT_FOLDER_L2, 'lsqSpec_final.txt');% save spectra
        save(dataname,'spec','-ascii');
        dataname = fullfile(OUTPUT_FOLDER_L2, 'lsqPara_final.csv');% save parameter
        T = array2table(parameter_set);
        T.Properties.VariableNames = varNames;
        writetable(T, dataname);
        dataname = fullfile(OUTPUT_FOLDER_L2, 'lsqMu_final.csv');% save mu
        T = array2table(mu_set);
        T.Properties.VariableNames = varNames2;
        writetable(T, dataname);
        if do_MC_sim==1
            try
                movefile('data/GPUMC_input.txt', fullfile(OUTPUT_FOLDER_L2, 'final_MC_input.txt'))
                movefile('data/GPUMC_output.txt',fullfile(OUTPUT_FOLDER_L2, 'final_MC_output.txt'))
            catch exception
                disp('Can''t move final_MC_input.txt, final_MC_output.txt')
            end
        end

        % plot and save piciture, KAO modified
        figure('Position',[0, 50, 1920, 1080]);
        sds_name = [4.5 7.5 10.5];
        xp = 700:880;
        for i=1:size(sds_choose,2)
            subplot(1, size(sds_choose,2), i);
            hold on
%             tar_y = spline(lambda, spec_target(:, i), xp);
%             fit_y = spline(lambda, spec(:, i), xp);
            tar_y = spec_target(:, i);
            fit_y = spec(:, i);
%             plot(xp, tar_y, 'LineWidth', 2);
%             plot(xp, fit_y, 'LineWidth', 2);
            plot(lambda, tar_y, 'LineWidth', 2);
            plot(lambda, fit_y, 'LineWidth', 2);
            if do_MC_sim==1            
                sds_mcml=[1 2 3];
                mc_y = spline(lambda, MC_spec(1:end-rw,sds_mcml(sds_choose(i))), xp);
                plot(xp, mc_y, 'LineWidth', 2);
            end
            xlabel('Wavelength (nm)');
            ylabel('Reflectance');
            xticks(linspace(700, 880, 10));
%             yticks(linspace(0, 1.2*max([tar_y fit_y]), 9));
            yticks(linspace(0, 3e-8, 7));
            ytickformat('%.1f')
            set(gca,'fontsize', 16) 
            grid on
%             title(['fitted result SDS' num2str(sds_choose(i))]);
            title(['SDS = ' num2str(sds_name(i)) ' mm']);
            if do_MC_sim==1
                legend({'Target' 'Fitted' 'MC'},'location','Best');
            else
                legend({'Target' 'Fitted'},'location','Best');
            end
        end
        hold off
        print(fullfile(OUTPUT_FOLDER_L2, 'fitted_result.png'), '-dpng');
%         saveas(gcf, fullfile(OUTPUT_FOLDER_L2, 'fitted_result.png'));
        close(gcf);
    end
end

function [mu] = Mu_generator(para, wl, epicell)
    global fitThickness thick lambda wl_all
    mu_epi = epicell{1};
    mu_mel = epicell{2};
    epsilon_oxy = epicell{3};
    epsilon_deoxy = epicell{4};
    mu_water = epicell{5};
    mu_collagen = epicell{6};
    mu_lipid = epicell{7};
    mu_epi = interp1(wl_all, mu_epi(:, 1), wl);
    mu_mel = interp1(wl_all, mu_mel(:, 1), wl);
    epsilon_oxy = interp1(wl_all, epsilon_oxy(:, 1),  wl);
    epsilon_deoxy = interp1(wl_all, epsilon_deoxy(:, 1),  wl);
    mu_water = interp1(wl_all,mu_water(:, 1),  wl, 'linear', 'extrap');
    mu_collagen = interp1( wl_all, mu_collagen(:, 1), wl);
    mu_lipid = interp1( wl_all, mu_lipid(:, 1), wl);
    th1 = repmat(thick(1), size(wl));
    th2 = repmat(thick(2), size(wl));
    th3 = repmat(thick(3), size(wl));
    f_mel = para(1);
    Chb2 = para(2);
    alpha2 = para(3);
    Chb3 = para(4);
    alpha3 = para(5);
    Chb4 = para(6);
    alpha4 = para(7);
    A1 = para(8);
    k1 = para(9);
    A2 = para(10);
    k2 = para(11);
    A3 = para(12);
    k3 = para(13);
    A4 = para(14);
    k4 = para(15);
%     fwater2 = para(20);
%     fwater3 = para(21);
%     fwater4 = para(22);
    fcol2 = para(16);
    flipid3 = para(17);
    flipid4 = para(18);

    mua1 = f_mel * mu_mel;
    mua2 = (2.303*Chb2*(alpha2*epsilon_oxy + (1-alpha2)*epsilon_deoxy)/64500) + 0.7*mu_water + fcol2*mu_collagen;
    mua3 = (2.303*Chb3*(alpha3*epsilon_oxy + (1-alpha3)*epsilon_deoxy)/64500) + 0.1*mu_water + flipid3*mu_lipid;
    mua4 = (2.303*Chb4*(alpha4*epsilon_oxy + (1-alpha4)*epsilon_deoxy)/64500) + 0.7*mu_water + flipid4*mu_collagen;
%     mua2 = f_blood2 * (2.303*Chb*(alpha2*epsilon_oxy + (1-alpha2)*epsilon_deoxy)/64500) + 0.7*mu_water + 0.2*mu_collagen;
%     mua3 = f_blood3 * (2.303*Chb*(alpha3*epsilon_oxy + (1-alpha3)*epsilon_deoxy)/64500) + 0.1*mu_water + 0.9*mu_lipid;
%     mua4 = f_blood4 * (2.303*Chb*(alpha4*epsilon_oxy + (1-alpha4)*epsilon_deoxy)/64500) + 0.7*mu_water + 0.2*mu_collagen;
%     mus1 = 1000*A1 * lambda(:,1).^-k1;
%     mus2 = 1000*A2 * lambda(:,1).^-k2;
%     mus3 = 1000*A3 * lambda(:,1).^-k3;
%     mus4 = 1000*A4 * lambda(:,1).^-k4;
    mus1 = A1 * (wl(:,1)/800).^-k1;
    mus2 = A2 * (wl(:,1)/800).^-k2;
    mus3 = A3 * (wl(:,1)/800).^-k3;
    mus4 = A4 * (wl(:,1)/800).^-k4;
    if fitThickness
    mu = [th1 th2 th3 mus1 mus2 mus3 mus4 mua1 mua2 mua3 mua4];
    else
    mu = [mus1 mus2 mus3 mus4 mua1 mua2 mua3 mua4];
    end
end

function [state,options,optchanged] = gaoutfun(options,state,flag)
global OUTPUT_FOLDER_L2 
global Lbound Ubound varName
persistent h1 
optchanged = false;
lb =  Lbound(4:end);
ub =  Ubound(4:end);
P = state.Population;
P = P(:, 4:end);
switch flag
    case 'init'
        h1 = figure('Position',[0, 50, 1280, 720]);
        for i = 1:8
            subplot(2, 4, i);
            hold on
            indexX = 2*i - 1;
            indexY = indexX + 1;
%             scatter(P(:, indexX), P(:, indexY), 'DisplayName', num2str(state.Generation));
            xlabel(varName{indexX});
            ylabel(varName{indexY});
            ax = gca;
            r = rectangle(ax,'Position',[lb(indexX) lb(indexY) ub(indexX)-lb(indexX) ub(indexY)-lb(indexY)]);
            ax.XLim = [0.8*lb(indexX) 1.2*ub(indexX)];
            ax.YLim = [0.8*lb(indexY) 1.2*ub(indexY)];
            if i == 4
                h = legend();
                rect = [0.92, 0.1, .05, .75];
                set(h, 'Position', rect);
            end
        end
        figure(gcf);
    case 'interrupt'
%         state.StopFlag = 'y';
        if mod(state.Generation, 50) == 0 && state.Generation ~= 0
            for i = 1:8
                subplot(2, 4, i);
                hold on
                indexX = 2*i - 1;
                indexY = indexX + 1;
                scatter(P(:, indexX), P(:, indexY), 'DisplayName', num2str(state.Generation));
                xlabel(varName{indexX});
                ylabel(varName{indexY});
                ax = gca;
                ax.XLim = [0.8*lb(indexX) 1.2*ub(indexX)];
                ax.YLim = [0.8*lb(indexY) 1.2*ub(indexY)];
            end
            figure(gcf);
        end
        % Update the fraction of mutation and crossover after 25 generations.
        if state.Generation == 1800
            options.CrossoverFraction = 0.8;
            optchanged = true;
        end
        if state.Generation == 1900
            state.StopFlag = 'y';
        end
%         % Find the best objective function, and stop if it is low.
%         ibest = state.Best(end);
%         ibest = find(state.Score == ibest,1,'last');
%         bestx = state.Population(ibest,:);
%         bestf = fun_MC_two_layer(bestx);
%         if bestf <= 0.1
%             state.StopFlag = 'y';
%             disp('Got below 0.1')
%         end
    case 'iter'
%         state.StopFlag = 'y';
        % Update the history every 10 generations.
        disp('iter')
    case 'done'
        hold off
        print(fullfile(OUTPUT_FOLDER_L2, 'history.png'), '-dpng');
        % Include the final population in the history.
%         ss = size(history,3);
%         history(:,:,ss+1) = state.Population;
%         assignin('base','gapopulationhistory',history);
end
end

function y = customSinc(x) 
    y = zeros(size(x));
    for i = 1:size(x,2)
    % 確保 x 不等於零，以避免除以零的錯誤
        if x(i) == 0
            y(i) = 1;
        else
            y(i) = sin(pi*x(i)) / (pi*x(i));
        end
    end
end