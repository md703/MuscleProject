%% combine database param and spec to .mat
clc; clear; close all;
%  load('fitting_program/data/20180524_database.mat','Spec','initial_param','wavelength_database');

addThickness = true;
% PATH
input_folder = 'database20w_euby_neck1221nb';
OUTPUT_NAME = 'database20w_euby_neck1221nb.mat';

fid = load(fullfile(input_folder, 'db_param.mat'), "-mat");
feps = load(fullfile(input_folder, 'epsilon.txt')); 
% wl = load('2023_0422_1523_wl.txt');
wl = load('20231113wavelength_points_all.txt')';

fparam = fid.db_param;
num_db_spec = size(fparam, 1);
num_sds = 3;
num_wl = size(wl, 2);

output_folder = fullfile(input_folder, 'wmc');
if ~exist(output_folder, 'dir')
    mkdir(output_folder)
end


% load ANN Model
load(fullfile('..', 'ANN_model', '5_neck_SDS_1-3.mat'), 'net');
% load(fullfile('..', 'ANN_model', 'SDS_1-12-3.mat'), 'net');
db = zeros(num_db_spec, num_wl, num_sds+1);

tic; time1 = toc;
%%
for i = 1:num_db_spec
    if i == 1 disp('Start !');end
    time2 = toc;
    wl = fparam(i, :, 1)';
    mus1 = fparam(i, :, 2)';
    mus2 = fparam(i, :, 3)';
    mus3 = fparam(i, :, 4)';
    mus4 = fparam(i, :, 5)';
    mua1 = fparam(i, :, 6)';
    mua2 = fparam(i, :, 7)';
    mua3 = fparam(i, :, 8)';
    mua4 = fparam(i, :, 9)';
    if addThickness
        th1 = repmat(feps(i, 2), size(wl, 1), 1);
        th2 = repmat(feps(i, 3), size(wl, 1), 1);
        th3 = repmat(feps(i, 4), size(wl, 1), 1);
        param = [th1 th2 th3 mus1 mus2 mus3 mus4 mua1 mua2 mua3 mua4];
    else
        param = [mus1 mus2 mus3 mus4 mua1 mua2 mua3 mua4];
    end
    spec = double(predict(net, param));
%     spec = power(10, -spec);
    spec = exp(-spec);

    time3 = toc - time2;
    disp(['Total count = ' num2str(time3) ' s'])
    fprintf('Run spectrum %5d / %5d\n', i, num_db_spec);
    spec = [wl spec];
    db(i, :, :) = spec;
end
save(fullfile(input_folder, 'db.mat'), 'db', '-mat');
disp('Finished !')

%% Output setting
initial_param = feps;
initial_param = initial_param(:, 2:end);
wavelength_database = wl';
Spec = load(fullfile(input_folder, 'db.mat'), "-mat", 'db');
Spec = Spec.db;
Spec = Spec(:, :, 2:end);
save(OUTPUT_NAME, 'Spec', 'initial_param', 'wavelength_database')
    