%%
% ANN param generation
% created by LEE, HAO-WEI 2022/9/22
clear; clc; close all;

%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% cm^-1
% param_name={'th1'  'mua1'  'mus1'  'th2'  'mua2'  'mus2'  'th3'  'mua3'  'mus3' 'mua4' 'mus4'}; %for 3layer
% lb =       [0.01    0.18    90      0.08   0.01    140     0.08   0.06    80     0.01   20]'; % lower boundary
% ub =       [0.01    35      580     0.42   2       330     0.62   2       270    1      100]'; % upper boundary
% sp =       [1       3       2       5      10      5       5      10      5      10     9]'; % sample points
% T = table(lb, ub, sp,'RowNames', param_name');
param_name={'th1'  'mua1'  'mus1'  'th2'  'mua2'  'mus2'  'th3'  'mua3'  'mus3' 'mua4' 'mus4'}; %for 3layer
lb =       [0.01    0.18    90      0.05   0.01    10     0.05   0.06    10     0.01   1]'; % lower boundary
ub =       [0.01    35      580     0.2    2       300    0.2   2      300    1      100]'; % upper boundary
sp =       [1       3       2       3      10      3       3      10      3      10     5]'; % sample points
T = table(lb, ub, sp,'RowNames', param_name');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% process thick
th1 = linspace(T{"th1","lb"}, T{"th1","ub"}, T{"th1","sp"}); th2 = linspace(T{"th2","lb"}, T{"th2","ub"}, T{"th2","sp"});
th3 = linspace(T{"th3","lb"}, T{"th3","ub"}, T{"th3","sp"});
rows = T{"th1","sp"} * T{"th2","sp"} * T{"th3","sp"}; cols = 4; 
th_arr = zeros(rows, cols);

id = 1;
for i = 1:length(th1)
    for j = 1:length(th2)
        for ii = 1:length(th3)
            th_arr(id, :) = [id th1(i) th2(j) th3(ii)];
            id = id + 1;
        end
    end
end
filename = [datestr(now,'yyyy_mmdd'), '_thick' num2str(rows) '.txt'];
save(filename, 'th_arr', '-ascii');

%% process mua
mua1 = linspace(T{"mua1","lb"}, T{"mua1","ub"}, T{"mua1","sp"}); mua2 = linspace(T{"mua2","lb"}, T{"mua2","ub"}, T{"mua2","sp"});
mua3 = linspace(T{"mua3","lb"}, T{"mua3","ub"}, T{"mua3","sp"}); mua4 = linspace(T{"mua4","lb"}, T{"mua4","ub"}, T{"mua4","sp"});
rows = T{"mua1","sp"} * T{"mua2","sp"} * T{"mua3","sp"} * T{"mua4","sp"}; cols = 5; 
mua_arr = zeros(rows, cols);

id = 1;
for i = 1:length(mua1)
    for j = 1:length(mua2)
        for ii = 1:length(mua3)
            for jj = 1:length(mua4)
                mua_arr(id, :) = [id mua1(i) mua2(j) mua3(ii) mua4(jj)];
                id = id + 1;
            end
        end
    end
end
filename = [datestr(now,'yyyy_mmdd'), '_mua' num2str(rows) '.txt'];
save(filename, 'mua_arr', '-ascii');

%% process mus
mus1 = linspace(T{"mus1","lb"}, T{"mus1","ub"}, T{"mus1","sp"}); mus2 = linspace(T{"mus2","lb"}, T{"mus2","ub"}, T{"mus2","sp"});
mus3 = linspace(T{"mus3","lb"}, T{"mus3","ub"}, T{"mus3","sp"}); mus4 = linspace(T{"mus4","lb"}, T{"mus4","ub"}, T{"mus4","sp"});
rows = T{"mus1","sp"} * T{"mus2","sp"} * T{"mus3","sp"} * T{"mus4","sp"}; cols = 5; 
mus_arr = zeros(rows, cols);

id = 1;
for i = 1:length(mus1)
    for j = 1:length(mus2)
        for ii = 1:length(mus3)
            for jj = 1:length(mus4)
                mus_arr(id, :) = [id mus1(i) mus2(j) mus3(ii) mus4(jj)];
                id = id + 1;
            end
        end
    end
end
filename = [datestr(now,'yyyy_mmdd'), '_mus' num2str(rows) '.txt'];
save(filename, 'mus_arr', '-ascii');

disp('Finished !')
