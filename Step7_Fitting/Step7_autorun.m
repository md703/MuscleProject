clc; clear; close all;

%% ####### Parameter define #########
global sds_choose do_MC_sim num_init rel_intensity area_dect ADD_NOISE net fitThickness
global fid_epi fid_mel fid_hemo fid_water fid_collagen fid_lipid 
global Spec initial_param wavelength_database lambda NOISE_PATH  folder_index spec_id

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% sds 1   2   3   4   5   6   7   8   9   10   11   12
%    0.2 0.4 0.6  2   3   4   5   6   7    8    9   10 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Default
% sds_all = {[7 9 12]};
% sds_all = {[8 10 12]; [2 4 7 10]; [2 6 9 12]; [4 7 10]; [5 8 11]; [6 9 12]};
sds_all = {[1 2 3]};
% sds_all = {[2 3]};
% sds_all = {[1]};

do_MC_sim = 0;              % do MC = 1, else = 0
num_init = 20;               % number of initial value choose from database
fitThickness = true;
ADD_NOISE = false;          % add random noise for target spectrum
IN_VIVO = true;            % fitting in-vivo spectrum = true, else = false
folder_index = 0;
% INPUT_FOLDER_LIST = {'syu_arterial_1006_dilated' 'syu_venous_1006_dilated' 'eu_arterial_1016_dilated' 'eu_venous_1016_dilated' 'kb_arterial_1026_dilated' 'kb_venous_1026_dilated'}
% OUTPUT_FOLDER_NAME_LIST = {'syu_arterial_1006_dilated_chb5_no_restriction' 'syu_venous_1006_dilated_chb5_no_restriction' 'eu_arterial_1016_dilated_chb5_no_restriction' 'eu_venous_1016_dilated_chb5_no_restriction' 'kb_arterial_1026_dilated_chb5_no_restriction' 'kb_venous_1026_dilated_chb5_no_restriction'}
% ANN_PATH_LIST = {'ANN_syu_forearm1006.mat' 'ANN_syu_forearm1006.mat' 'ANN_eu_forearm1016.mat' 'ANN_eu_forearm1016.mat' 'ANN_kb_forearm1026.mat' 'ANN_kb_forearm1026.mat' }
% DB_PATH_LIST = {'database5w_20231006_syu.mat' 'database5w_20231006_syu.mat' 'database5w_20231016_eu.mat' 'database5w_20231016_eu.mat' 'database5w_20231026_kb.mat' 'database5w_20231026_kb.mat'}

% INPUT_FOLDER_LIST = {'kb_arterial_1026_dilated' 'kb_venous_1026_dilated'}
% OUTPUT_FOLDER_NAME_LIST = {'kb_arterial_1026_dilated_no_restriction' 'kb_venous_1026_dilated_no_restriction'}
% ANN_PATH_LIST = {'ANN_kb_forearm1026.mat' 'ANN_kb_forearm1026.mat' }
% DB_PATH_LIST = {'database5w_20231026_kb.mat' 'database5w_20231026_kb.mat'}

% INPUT_FOLDER_LIST = {'eu_neck1016', 'by_neck1102'}
% OUTPUT_FOLDER_NAME_LIST = {'eu_neck1016_dilated', 'by_neck1102_dilated'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat', '5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database5w_euby_neck.mat', 'database5w_euby_neck.mat'}

% INPUT_FOLDER = 'Invivo/kb_arterial_1026_dilated';      % target spectrum path
% OUTPUT_FOLDER_NAME = 'kb_arterial_1026_dilated';
% ANN_PATH = fullfile('data', 'ANN_model', 'ANN_kb_forearm.mat');


% INPUT_FOLDER_LIST = {'kb_neck1026' 'eu_neck1016', 'by_neck1102'}
% OUTPUT_FOLDER_NAME_LIST = {'kb_neck1026_dilated_db20w_sp72319' 'eu_neck1016_dilated_db20w_sp72319', 'by_neck1102_dilated_db20w_sp72319'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat', '5_neck_SDS_1-3.mat', '5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database20w_kb_neck.mat', 'database20w_euby_neck.mat', 'database20w_euby_neck.mat'}

% INPUT_FOLDER_LIST = {'eu_neck1016', 'by_neck1102'}
% OUTPUT_FOLDER_NAME_LIST = {'eu_neck1016_dilated_db20w1222', 'by_neck1102_dilated_db20w1222'}
% ANN_PATH_LIST = { '5_neck_SDS_1-3.mat', '5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = { 'database20w_euby_neck1221nb.mat', 'database20w_euby_neck1221nb.mat'}

% INPUT_FOLDER_LIST = {'kb_neck1026'}
% OUTPUT_FOLDER_NAME_LIST = {'kb_neck1026_dilated_db20w_1221'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database20w_kb_neck1221nb.mat'}

% INPUT_FOLDER_LIST = {'kb_test'}
% OUTPUT_FOLDER_NAME_LIST = {'kb_test'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database20w_kb_neck1221nb.mat'}

% INPUT_FOLDER_LIST = {'eu_test'}
% OUTPUT_FOLDER_NAME_LIST = {'eu_test'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database20w_euby_neck1221nb.mat'}

% INPUT_FOLDER_LIST = {'kb_test','eu_test'}
% OUTPUT_FOLDER_NAME_LIST = {'kb_test','eu_test'}
% ANN_PATH_LIST = {'5_neck_SDS_1-3.mat','5_neck_SDS_1-3.mat'}
% DB_PATH_LIST = {'database20w_kb_neck1221nb.mat','database20w_euby_neck1221nb.mat'}


INPUT_FOLDER_LIST = {'by_test'}
OUTPUT_FOLDER_NAME_LIST = {'by_test'}
ANN_PATH_LIST = {'5_neck_SDS_1-3.mat'}
DB_PATH_LIST = {'database20w_euby_neck1221nb.mat'}


% prefit baseline
% INPUT_FOLDER_LIST = {'syu_baseline_prefit__dilated_arterial' 'syu_baseline_prefit__dilated_venous', 'eu_baseline_prefit__dilated_arterial', 'eu_baseline_prefit__dilated_venous', 'kb_baseline_prefit__dilated_arterial', 'kb_baseline_prefit__dilated_venous'}
% OUTPUT_FOLDER_NAME_LIST = {'syu_baseline_prefit__dilated_arterial_fix' 'syu_baseline_prefit__dilated_venous_fix', 'eu_baseline_prefit__dilated_arterial_fix', 'eu_baseline_prefit__dilated_venous_fix', 'kb_baseline_prefit__dilated_arterial_fix', 'kb_baseline_prefit__dilated_venous_fix'}
% ANN_PATH_LIST = {'ANN_syu_forearm1006.mat', 'ANN_syu_forearm1006.mat', 'ANN_eu_forearm1016.mat', 'ANN_eu_forearm1016.mat', 'ANN_kb_forearm1026.mat', 'ANN_kb_forearm1026.mat'}
% DB_PATH_LIST = {'database5w_20231006_syu_arterial.mat', 'database5w_20231006_syu_venous.mat', 'database5w_20231016_eu_arterial.mat', 'database5w_20231016_eu_venous.mat', 'database5w_20231026_kb_arterial.mat', 'database5w_20231026_kb_venous.mat'}

% prefit occlusion
% INPUT_FOLDER_LIST = {'syu_occlusion_prefit__dilated_arterial' 'syu_occlusion_prefit__dilated_venous', 'eu_occlusion_prefit__dilated_arterial', 'eu_occlusion_prefit__dilated_venous', 'kb_occlusion_prefit__dilated_arterial', 'kb_occlusion_prefit__dilated_venous'}
% OUTPUT_FOLDER_NAME_LIST = {'syu_occlusion_prefit__dilated_arterial_fix' 'syu_occlusion_prefit__dilated_venous_fix', 'eu_occlusion_prefit__dilated_arterial_fix', 'eu_occlusion_prefit__dilated_venous_fix', 'kb_occlusion_prefit__dilated_arterial_fix', 'kb_occlusion_prefit__dilated_venous_fix'}
% ANN_PATH_LIST = {'ANN_syu_forearm1006.mat', 'ANN_syu_forearm1006.mat', 'ANN_eu_forearm1016.mat', 'ANN_eu_forearm1016.mat', 'ANN_kb_forearm1026.mat', 'ANN_kb_forearm1026.mat'}
% DB_PATH_LIST = {'database5w_20231006_syu_arterial.mat', 'database5w_20231006_syu_venous.mat', 'database5w_20231016_eu_arterial.mat', 'database5w_20231016_eu_venous.mat', 'database5w_20231026_kb_arterial.mat', 'database5w_20231026_kb_venous.mat'}

% prefit release
% INPUT_FOLDER_LIST = {'syu_release_prefit__dilated_arterial' 'syu_release_prefit__dilated_venous', 'eu_release_prefit__dilated_arterial', 'eu_release_prefit__dilated_venous', 'kb_release_prefit__dilated_arterial', 'kb_release_prefit__dilated_venous'}
% OUTPUT_FOLDER_NAME_LIST = {'syu_release_prefit__dilated_arterial_fix' 'syu_release_prefit__dilated_venous_fix', 'eu_release_prefit__dilated_arterial_fix', 'eu_release_prefit__dilated_venous_fix', 'kb_release_prefit__dilated_arterial_fix', 'kb_release_prefit__dilated_venous_fix'}
% ANN_PATH_LIST = {'ANN_syu_forearm1006.mat', 'ANN_syu_forearm1006.mat', 'ANN_eu_forearm1016.mat', 'ANN_eu_forearm1016.mat', 'ANN_kb_forearm1026.mat', 'ANN_kb_forearm1026.mat'}
% DB_PATH_LIST = {'database5w_20231006_syu_arterial.mat', 'database5w_20231006_syu_venous.mat', 'database5w_20231016_eu_arterial.mat', 'database5w_20231016_eu_venous.mat', 'database5w_20231026_kb_arterial.mat', 'database5w_20231026_kb_venous.mat'}

% INPUT_FOLDER_LIST = {'syu_arterial_1006_dilated' 'syu_venous_1006_dilated' 'eu_arterial_1016_dilated' 'eu_venous_1016_dilated' 'kb_arterial_1026_dilated' 'kb_venous_1026_dilated'}
% OUTPUT_FOLDER_NAME_LIST = {'syu_arterial_1006_dilated_3stage_new' 'syu_venous_1006_dilated_3stage_new2' 'eu_arterial_1016_dilated_3stage_new' 'eu_venous_1016_dilated_3stage_new2' 'kb_arterial_1026_dilated_3stage_new' 'kb_venous_1026_dilated_3stage_new2'}
% ANN_PATH_LIST = {'ANN_syu_forearm1006.mat' 'ANN_syu_forearm1006.mat' 'ANN_eu_forearm1016.mat' 'ANN_eu_forearm1016.mat' 'ANN_kb_forearm1026.mat' 'ANN_kb_forearm1026.mat' }
% DB_PATH_LIST = {'database5w_20231006_syu.mat' 'database5w_20231006_syu.mat' 'database5w_20231016_eu.mat' 'database5w_20231016_eu.mat' 'database5w_20231026_kb.mat' 'database5w_20231026_kb.mat'}
NOISE_PATH = 'cv_channel.csv';
% DB_PATH = fullfile('data', 'database5w_20231026_kb.mat');
% ###################################
% load file
% load spectrum of absorbent 
fid_epi = load('../Epsilon/mu_epi.txt');
fid_mel = load('../Epsilon/mel_mua.txt');
fid_hemo = load('../Epsilon/epsilon.txt');
fid_water = load('../Epsilon/water_mua.txt');
fid_collagen = load('../Epsilon/collagen_mua.txt');
fid_lipid = load('../Epsilon/subcutaneous_mua.txt');
lambda = load(fullfile('data', '20231227wavelength_points_all.txt'));         % fitting wavelength

for folder_index = 1:size(INPUT_FOLDER_LIST, 2)
%     if folder_index == 2 || folder_index == 4 || folder_index == 6
%         continue
%     end
    INPUT_FOLDER = fullfile('Invivo', INPUT_FOLDER_LIST{folder_index})
    OUTPUT_FOLDER_NAME = OUTPUT_FOLDER_NAME_LIST{folder_index}
    ANN_PATH = fullfile('data', 'ANN_model', ANN_PATH_LIST{folder_index})
    DB_PATH = fullfile('data', DB_PATH_LIST{folder_index});
    
    load(ANN_PATH, 'net');                                      % load Forward model
    load(DB_PATH,'Spec','initial_param','wavelength_database');    % database for choosing init value
    
    
    % input target list
    file_list = dir(INPUT_FOLDER);
    filename_arr={};
    for i=1:length(file_list)
        if file_list(i).isdir==0
            filename_arr = [filename_arr file_list(i).name];
        end
    end
    
    
    % fitting each sds set
    for j = 1:size(sds_all, 1)
        tic;
        t1 = toc;
        sds_choose = sds_all{j};
    
        
        disp(['SDS ' num2str(j) '/' num2str(size(sds_all, 1)) ': ' num2str(sds_choose)]);
        for spec_id=1:length(filename_arr)
            disp(['fitting ' num2str(spec_id) '/' num2str(length(filename_arr)) ': ' strtok(filename_arr{spec_id},'.')]);
            fun_main(fullfile(INPUT_FOLDER, filename_arr{spec_id}), strtok(filename_arr{spec_id}, '.'), OUTPUT_FOLDER_NAME);
        end
        
        if IN_VIVO == true
            break;
        else
            % Accuracy each sds
            sds_str = strjoin(string(sds_choose), '_');
            PRED_FOLDER = convertStringsToChars("sds_" + sds_str);
            TARGET_FOLDER = 'Target_Spec_20221021';
            errCalculate(length(filename_arr), PRED_FOLDER, TARGET_FOLDER);
            mkdir(PRED_FOLDER);
            [success1, msg, msgID] = movefile(['*.csv'], PRED_FOLDER, 'f');
            [success2, msg, msgID] = movefile(['*.png'], PRED_FOLDER, 'f');
            [success3, msg, msgID] = movefile(['simspec*'], PRED_FOLDER, 'f');
            if (~success1 & ~success2)
                disp('Move error !')
                pause(10);
                [success1, msg, msgID] = movefile(['*.csv'], PRED_FOLDER, 'f');
                [success2, msg, msgID] = movefile(['*.png'], PRED_FOLDER, 'f');
            end
            t2 = toc;
            fprintf('Cost %.2f seconds!\n', t2-t1);
        end
    end
end


disp('Auto Fitting Done!');