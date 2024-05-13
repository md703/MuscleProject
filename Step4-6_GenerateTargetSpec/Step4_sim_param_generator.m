%% This can generate param of simulated spectrum
%  2022/6/14 created by LEE, HAO-WEI
clear; clc; close all;

% parforWaitbar();
% 
% function a = parforWaitbar
addThickness = true;
fix_hb = true;
rng('default');
num_spec = 201000;
% num_spec = 1100;
num_fit = 1000;
num_database = num_spec - num_fit;
fit_folder = 'Target_Spec_20231026_kb';
database_folder = 'database20w_euby_neck1221nb';

if ~(exist(fit_folder, "dir"))
    mkdir(fit_folder)
end
if ~(exist(database_folder, "dir"))
    mkdir(database_folder)
end

% wl = [700 708 716 724 732 739 745 752 759 769 779 788 798 805 812 820 826 832 840 854 866 880];
wl =[700	708	716	724	732	739	742	745	752	755	757	759	761	763	769	779	788	798	805	812	820	826	832	840	854	866	880];

save([datestr(now,'yyyy_mmdd_HHMM') '_wl.txt'], 'wl', '-ascii');

fid_epi = load('../Epsilon/mu_epi.txt');
fid_mel = load('../Epsilon/mel_mua.txt');
fid_hemo = load('../Epsilon/epsilon.txt');
fid_water = load('../Epsilon/water_mua.txt');
fid_collagen = load('../Epsilon/collagen_mua.txt');
fid_lipid = load('../Epsilon/subcutaneous_mua.txt');

mu_epi = interp1(fid_epi(:, 1), fid_epi(:, 2), wl);
mu_mel = interp1(fid_mel(:, 1), fid_mel(:, 2), wl);
epsilon_oxy = interp1(fid_hemo(:, 1), fid_hemo(:, 2), wl);
epsilon_deoxy = interp1(fid_hemo(:, 1), fid_hemo(:, 3), wl);
mu_water = interp1(fid_water(:, 1), fid_water(:, 2), wl);
mu_collagen = interp1(fid_collagen(:, 1), fid_collagen(:, 2), wl);
mu_lipid = interp1(fid_lipid(:, 1), fid_lipid(:, 2), wl);


%%
% param bound cm^-1
%       f_mel    Chb   f_blood2   alpha2  f_blood3   alpha3    f_blood4    alpha4    A1         k1       A2       k2      A3      k3      A4       k4
% lb =    [0.001   100    0.002      0       0.002        0        0.002        0       10        1.001     10     1.001     10     1.001     3      1.1];
% ub =    [0.008   180    0.04       1       0.04         1        0.04         1       500        1.5      500     1.5      500     1.5      30      1.3];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% cm^-1 
if addThickness
    if fix_hb
        param_name={'th1'  'th2'            'th3'               'f_mel'  'Chb2'  'alpha2' 'Chb3' 'alpha3'  'Chb4'  'alpha4'  'A1'    'k1'    'A2'       'k2'     'A3'    'k3'    'A4'    'k4' 'fcol2' 'flipid3' 'fprotein4'}; %for 3layer
    else
        param_name={'th1'  'th2'            'th3'               'f_mel'  'Chb2'  'alpha2' 'Chb3' 'alpha3'  'Chb4'  'alpha4'  'A1'    'k1'    'A2'       'k2'     'A3'    'k3'    'A4'    'k4' 'fcol2' 'flipid3' 'fprotein4'}; %for 3layer
    end

else
    param_name={'f_mel'  'Chb2'  'alpha2' 'Chb3' 'alpha3'  'Chb4'  'alpha4'  'A1'    'k1'    'A2'       'k2'     'A3'    'k3'    'A4'    'k4' 'fcol2' 'flipid3' 'fprotein4'}; %for 3layer
end
% 1026 kb forearm
% lb =        [0.001    0.12     0     0.12      0        0.12     0       10      0.58    0.78       0.24      1.8    0.68      4    0.61    0       0        0]'; % lower boundary
% ub =        [0.16     4.8      1     4.8       1        4.8      1       2662    1.41    10897      1.63      48     0.88    940    1.51    1       1        1]';
% lb =        [0.001    0.12     0     0.12      0        0.12     0       10      0.58    0.78       0.24      1.8    0.68      4    0.61    0.5       0.001        0.5]'; % lower boundary
% ub =        [0.16     60      1     60      1        60      1       2662    1.41    10897      1.63      48     0.88    940    1.51    0.5       0.01        0.5]';
% lb =        [0.001    0.12     0     0.12      0        0.12     0       123    0.58    156      0.24      110    0.68     38    0.61    0       0        0]'; % lower boundary
% ub =        [0.16     20      1      20        1        20       1       398    1.41    218      1.63      196    0.88    70    1.51    1       1        1]';
% lb =        [0.01   0.145    0.068     0.001      120     0.001          0.5      0.001        0.5          0.001         0.5       10        0.58    0.78       0.24      1.8    0.68      4    0.61 0 0 0 0 0 0]'; % lower boundary
% ub =        [0.01   0.145    0.068     0.16       175     0.04           1        0.04         1            0.04          1         2662      1.41    10897      1.63      48     0.88    940    1.51 1 1 1 1 1 1]';
% param_name={'th1'  'th2'     'th3'    'f_mel'    'Chb'   'f_blood2'   'alpha2'  'f_blood3'   'alpha3'    'f_blood4'    'alpha4'    'A1'       'k1'    'A2'       'k2'     'A3'    'k3'    'A4'    'k4'}; %for 3layer
% lb =        [0.01   0.25    0.15     0.001      120     0.001          0.5      0.001        0.5          0.001         0.5       10        0.58    0.78       0.24      1.8    0.68      4    0.61]'; % lower boundary
% ub =        [0.01   0.25    0.15     0.16       175     0.04           1        0.04         1            0.04          1         2662      1.41    10897      1.63      48     0.88    940    1.51]';
% lb =       [0.01    0.049    0.276     0.013      120    0.002           0       0.002        0            0.002        0           23       0.58    8        0.5         28     0.7       4     0.61]'; % lower boundary
% ub =       [0.01    0.049    0.276     0.039      175    0.17            1       0.04         1            0.1          1           27       0.8     10        0.62       35      0.88    10     0.8]'; % upper boundary

% %       1006 syu arterial
%         lb = [0.143595	0	0	0	0	0	0	1506.502563	1.43445	4495.311523	1.877872	17.375437	0.725404	715.169312	1.608625	2	0.001015	1.999992]';
%         ub = [0.143595	20	1	20	1	20	1	1506.502563	1.43445	4495.311523	1.877872	17.375437	0.725404	715.169312	1.608625	2	0.001015	1.999992]';
% 
% %       1006 syu venous
%         lb = [0.005102	0	0	0	0	0	0	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634]';
%         ub = [0.005102	20	1	20	1	20	1	1520.705688	1.233278	4760.917969	1.778995	6.055368	0.91416	522.326172	1.579572	2	0.015237	1.998634]';
% 
% %       1016 eu arterial
%         lb = [0.038296	0	0	0	0	0	0	1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]';
%         ub = [0.038296	20	1	20	1	20	1	1431.291626	1.384645	4650.742676	1.903995	8.264904	0.725404	512.769653	1.579572	2	0.001783	1.998634]';
% 
% %       1016 eu venous
%         lb = [0.09158	0	0	0	0	0	0	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603]';
%         ub = [0.09158	20	1	20	1	20	1	1877.041626	1.413453	4626.214844	1.857425	47.93005	0.964941	708.906738	1.548322	1.999942	0	0.041603]';

        

%       1026 kb arterial
%         lb = [0.16	0	0	0	0	0	0	1657.428711	1.214723	4147.046875	1.907901	15.211372	0.964941	671.77063	1.345197	2	3.90E-05	1.999997]';
%         ub = [0.16	20	1	20	1	20	1	1657.428711	1.214723	4147.046875	1.907901	15.211372	0.964941	671.77063	1.345197	2	3.90E-05	1.999997]';

% %       1026 kb venous
%         lb = [0.16	0	0	0	0	0	0	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';
%         ub = [0.16	20	1	20	1	20	1	1615.552612	1.210817	4092.49292	1.905948	16.454636	0.981604	744.17572	1.360822	2	3.90E-05	1.999993]';

%        kb neck
% lb =        [0.01 0.18599 0.07488 0.001    0.12     0     0.12      0        0.12     0       10      0.58    0.78       0.24      1.8    0.68      4    0.61    0.5       0.001        0.5]'; % lower boundary
% ub =        [0.01 0.18599 0.07488 0.16     60      1     60      1        60      1       2662    1.41    10897      1.63      48     0.88    940    1.51    0.5       0.01        0.5]';
% lb =        [0.01 0.18599 0.07488 0.001    0.12     0     0.12   0        0.12     0       0      0    0       0      0     0      0    0    0.5       0.0001        0.5]'; % lower boundary
% ub =        [0.01 0.18599 0.07488 0.16     60      1     60      1        60       1       1000   4    1000    4      1000  4    1000   4    0.5       0.01        0.5]';

%       eu by  neck
% lb =        [0.01 0.1449 0.05314 0.001    0.12     0     0.12      0        0.12     0       10      0.58    0.78       0.24      1.8    0.68      4    0.61    0.5       0.001        0.5]'; % lower boundary
% ub =        [0.01 0.1449 0.05314 0.16     60       1     60       1         60       1       2662    1.41    10897      1.63      48     0.88    940    1.51    0.5       0.01        0.5]';
lb =        [0.01 0.1449 0.05314 0.001    0.12     0     0.12      0        0.12     0       0      0    0       0      0     0      0    0    0.5       0.0001        0.5]'; % lower boundary
ub =        [0.01 0.1449 0.05314 0.16     60       1     60       1         60       1       1000   4    1000    4      1000  4    1000   4     0.5       0.01        0.5]';
 
T = table(lb, ub,'RowNames', param_name');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% lb2 = [90     10    10     1     0.18   0.01   0.06   0.01];
% ub2 = [580    150    150    100    35     2      2      1 ];
lb2 = [90     1    1     1     0.18   0.01   0.06   0.01];
ub2 = [581    150    150    101    35     2      2      1 ];
epsilon = zeros(num_spec, size(param_name, 2) + 1);
param = zeros(num_spec, size(wl, 2), 9);

total = 0;
% 
% D = parallel.pool.DataQueue;
% h = waitbar(0, 'Please wait ...');
% afterEach(D, @nUpdateWaitbar);
% 
% p = 1;

for i = 1:num_spec
    % not in bound
%     op1 = true;
%     op2 = true;
%     while op1 == true || op2 == true
        if addThickness
            th1 = random_select(T{'th1','lb'}, T{'th1','ub'});
            th2 = random_select(T{'th2','lb'}, T{'th2','ub'});
            th3 = random_select(T{'th3','lb'}, T{'th3','ub'});
        end
        f_mel = random_select(T{'f_mel','lb'}, T{'f_mel','ub'});
        Chb2 = random_select(T{'Chb2','lb'}, T{'Chb2','ub'});
        Chb3 = random_select(T{'Chb3','lb'}, T{'Chb3','ub'});
        Chb4 = random_select(T{'Chb4','lb'}, T{'Chb4','ub'});
        alpha2 = random_select(T{'alpha2','lb'}, T{'alpha2','ub'});
        alpha3 = random_select(T{'alpha3','lb'}, T{'alpha3','ub'});
        alpha4 = random_select(T{'alpha4','lb'}, T{'alpha4','ub'});
        A1 = random_select(T{'A1','lb'}, T{'A1','ub'});
        A2 = random_select(T{'A2','lb'}, T{'A2','ub'});
        A3 = random_select(T{'A3','lb'}, T{'A3','ub'});
        A4 = random_select(T{'A4','lb'}, T{'A4','ub'});
        k1 = random_select(T{'k1', 'lb'}, T{'k1','ub'});
        k2 = random_select(T{'k2', 'lb'}, T{'k2','ub'});
        k3 = random_select(T{'k3', 'lb'}, T{'k3','ub'});
        k4 = random_select(T{'k4', 'lb'}, T{'k4','ub'});
%         k1 = random_select(-log(ub2(1)/(1000*A1))/log(700), -log(lb2(1)/(1000*A1))/log(880));
%         k2 = random_select(-log(ub2(2)/(1000*A2))/log(700), -log(lb2(2)/(1000*A2))/log(880));
%         k3 = random_select(-log(ub2(3)/(1000*A3))/log(700), -log(lb2(3)/(1000*A3))/log(880));
%         k4 = random_select(-log(ub2(4)/(1000*A4))/log(700), -log(lb2(4)/(1000*A4))/log(880));
        fcol2 = random_select(T{'fcol2','lb'}, T{'fcol2','ub'});
        flipid3 = random_select(T{'flipid3','lb'}, T{'flipid3','ub'});
        fprotein4 = random_select(T{'fprotein4','lb'}, T{'fprotein4','ub'});
        mua1 = f_mel * mu_mel;
        mua2 = (2.303*Chb2*(alpha2*epsilon_oxy + (1-alpha2)*epsilon_deoxy)/64500) + 0.7*mu_water + fcol2*mu_collagen;
        mua3 = (2.303*Chb3*(alpha3*epsilon_oxy + (1-alpha3)*epsilon_deoxy)/64500) + 0.1*mu_water + flipid3*mu_lipid;
        mua4 = (2.303*Chb4*(alpha4*epsilon_oxy + (1-alpha4)*epsilon_deoxy)/64500) + 0.7*mu_water + fprotein4*mu_collagen;
%         mua2 = f_blood2 * (2.303*Chb*(alpha2*epsilon_oxy + (1-alpha2)*epsilon_deoxy)/64500) + 0.7*mu_water + (1 - 0.7 - f_blood2)*mu_collagen;
%         mua3 = f_blood3 * (2.303*Chb*(alpha3*epsilon_oxy + (1-alpha3)*epsilon_deoxy)/64500) + 0.1*mu_water + (1 - 0.1 - f_blood3)*mu_lipid;
%         mua4 = f_blood4 * (2.303*Chb*(alpha4*epsilon_oxy + (1-alpha4)*epsilon_deoxy)/64500) + 0.7*mu_water + (1 - 0.7 - f_blood4)*mu_collagen;      
%         mus1 = 1000*A1 * wl.^-k1;
%         mus2 = 1000*A2 * wl.^-k2;
%         mus3 = 1000*A3 * wl.^-k3;
%         mus4 = 1000*A4 * wl.^-k4;
        mus1 = A1 * (wl/800).^-k1;
        mus2 = A2 * (wl/800).^-k2;
        mus3 = A3 * (wl/800).^-k3;
        mus4 = A4 * (wl/800).^-k4;
        
        % test param in ANN range
%         annLb = [0.01  0.145  0.068  90     10    10     1     0.18   0.01   0.06   0.01 ];
%         annUb = [0.01  0.145  0.068  580    150    150    100    35     2      2      1 ];
        
%         test = [mus1' mus2' mus3' mus4' mua1' mua2' mua3' mua4' ];
% 
%         % not in bound
%         op1 = max(test < lb2, [], 'all');
%         op2 = max(test > ub2, [], 'all');
%     end
    param(i, :, :) = [wl' mus1' mus2' mus3' mus4' mua1' mua2' mua3' mua4'];
    if addThickness
        epsilon(i, :) = [i th1 th2 th3 f_mel Chb2 alpha2 Chb3 alpha3 Chb4 alpha4 A1 k1 A2 k2 A3 k3 A4 k4 fcol2 flipid3 fprotein4];
    else
        epsilon(i, :) = [i f_mel Chb2 alpha2 Chb3 alpha3 Chb4 alpha4 A1 k1 A2 k2 A3 k3 A4 k4 fcol2 flipid3 fprotein4];
    end
    if mod(i, 1000) == 0
        fprintf('Run spectrum %5d / %5d\n', i, num_spec);
    end
%         send(D, i);
end
%     function nUpdateWaitbar(~)
%             waitbar(p/num_spec, h);
%             p = p + 1;
%     end
db_param = param(1:num_database, :, :);
save(fullfile(database_folder, 'db_param.mat'), 'db_param', '-mat');
for i = 1 : num_fit               
    temp_param = squeeze(param(num_database+i, :, :));
    save([ fit_folder '/param_' num2str(i) '.txt'], 'temp_param', '-ascii');
end
temp_epi = epsilon(1:num_database, :);
save([ database_folder '/epsilon.txt'], 'temp_epi', '-ascii');
temp_epi = epsilon(num_database+1: end, :);
save([ fit_folder '/epsilon.txt'], 'temp_epi', '-ascii');

% Check duplicated
[C,ia,ic] = unique(epsilon(:,2:end),'rows');
if size(C, 1) == size(epsilon, 1) 
    disp('No duplicated !') 
end

disp('finished !')

% end
%%
function output = random_select(x1, x2)
    scalar = x2 - x1;
    p = rand();
    output = x1 + p*scalar;
end