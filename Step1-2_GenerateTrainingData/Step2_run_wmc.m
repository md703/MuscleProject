%%
% for caculate WMC reflectance
% created by Golson Lin 2020.07.09
% edited by LEE, HAO-WEI 2022/9/22
clc; close all; clear;

GPU_ID = 0;

%% folder
output_folder='tdata';
sim_set_file = 'sim_setup.json';
file_th = load('2023_0710_thick4.txt');
file_mua = load('2023_0710_mua3000.txt');
file_mus = load('2023_0710_mus450.txt');

% Check if output folder existed
if exist(output_folder) == 7
    disp([output_folder ' already exist!'])
    disp(['Press any key to contunue:'])
    pause;
end
 
%% parameter
MODE = 1;   % 1:sim   2:load  3:mua fixed (do not use)
PATR_NUM = 5; % initial part number e.g. 1/5
THRESHOLD_CV = 0.02 * sqrt(PATR_NUM); % CV = 2%
THRESHOLD_RUN = 30;
ZERO_MUA = 0;
a_arr = file_mua(:, 2:5);
s_arr = file_mus(:, 2:5);
th_arr = file_th(:, 2:4);
g_arr = [-1 0.715 0.9 0.93];
n_arr = [1.4 1.4 1.4 1.4];
NUM_MUA = size(a_arr, 1);
NUM_MUS = size(s_arr, 1);
NUM_THICK = size(th_arr, 1);
start_id = 1;
stop_id = 4;

%% load setting

sim_set = jsondecode(fileread(sim_set_file));
NUM_SDS = sim_set.probes.num_SDS;
NUM_LAYER = sim_set.number_layers;
NUM_PHOTONS = sim_set.number_photons;
spec = zeros(NUM_THICK, NUM_MUS, NUM_MUA, NUM_SDS);
param = [];
param_temp = zeros(1, 11);
PL = cell(NUM_SDS, 1);
PL_arr = cell(NUM_SDS, 1);
gpu_a = gpuArray(a_arr);
time_arr = []; tic; time1 = toc; % timer start

%% main
for id_thick = start_id:stop_id
    fprintf('Thick: %3.2f, %3.2f, %3.2f\n', th_arr(id_thick, 1), th_arr(id_thick, 2), th_arr(id_thick, 3))
    param_temp(1, 1:3) = th_arr(id_thick, :);
    time2 = toc; time3 = toc;
    for id_mus = 1:NUM_MUS
        % record CV previous 10 times
        cv_record = [100 100 100 100 100 100 100 100 100 1]; 
        CV_UPDATED = true;
        fprintf('time interval: %.2f\n', time2-time3); time3 = toc; time_arr = [time_arr time3-time2];
        fprintf('Thick NO.%d, Mus NO.%d :\n', id_thick, id_mus)
        PL(:) ={[]};
        run = 1;    % initial run_times
        part = PATR_NUM;
        NEXT_MUS = false;
        param_temp(1, 4:7) = s_arr(id_mus, :);
        ref_all = zeros(part, NUM_MUA, NUM_SDS, 50);
        while NEXT_MUS ~= true
            fprintf('\tprocess run: %d', run);
            folder=fullfile(output_folder,['thick_' num2str(id_thick)], ['mus_' num2str(id_mus)], ['run_' num2str(run)]);
            temp_param = [th_arr(id_thick, 1) ZERO_MUA s_arr(id_mus, 1) n_arr(1) g_arr(1)...
                        th_arr(id_thick, 2) ZERO_MUA s_arr(id_mus, 2) n_arr(2) g_arr(2)...
                        th_arr(id_thick, 3) ZERO_MUA s_arr(id_mus, 3) n_arr(3) g_arr(3)...
                                            ZERO_MUA s_arr(id_mus, 4) n_arr(4) g_arr(4)];
            if MODE == 1
                mkdir(folder); 
                copyfile('ledptn.txt', folder);
                copyfile('tissue_anglepattern.txt', folder);
                copyfile('tissue_anglepattern2.txt', folder);
                cd(folder);
                save('GPUMC_input.txt', 'temp_param', '-ascii', '-tabs');
                if ispc
                    [~, ~] = system('..\..\..\..\MCML_GPU_ANGLE.exe ..\..\..\..\sim_setup.json GPUMC_input.txt GPUMC_output.txt -R -P -B');
                elseif isunix
                    [~, ~] = system(['../../../../MCML_GPU_ANGLE ../../../../sim_setup.json GPUMC_input.txt GPUMC_output.txt -G ' num2str(GPU_ID) ' -R -P -B ']);
%                     [~, ~] = system('../../../../MCML_GPU_ANGLE ../../../../sim_setup.json GPUMC_input.txt GPUMC_output.txt -R -P -B');
                else
                    disp('Platform not supported')
                    exit
                end
                cd ../../../../;
            end
            sim_sum = jsondecode(fileread(fullfile(folder, 'summary.json'))); % if json allready exist, will crash
            detectphoton_number = zeros(NUM_SDS,1);
            fraction = zeros(NUM_SDS,1);
            remainder = zeros(NUM_SDS,1);
            
            % Calculate reflectance
            for s = 1:NUM_SDS
                PL{s} = load_binary_pathlength_output(fullfile(folder, 'summary.json'), s, fullfile(folder,['pathlength_SDS_' num2str(s) '.bin']));
                detectphoton_number(s) = length(PL{s});
                fraction(s)=floor(detectphoton_number(s)/part);
                remainder(s) = mod(detectphoton_number(s),part);
                gpu_pl = gpuArray(PL{s});
                for part_index = 1:part
                    if part_index == part
                        p = fraction(s)*(part_index-1)+1 : length(PL{s});
                        ref_all(part_index, :, s, run) = sum(gather(gpu_pl(p, 1).*exp(-gpu_pl(p, 2:5)*transpose(gpu_a(:, :))) ), 1) / (sim_sum.each_photon_weight/part);
                    else                                
                        p = fraction(s)*(part_index-1)+1 : fraction(s)*part_index;
                        ref_all(part_index, :, s, run) = sum(gather(gpu_pl(p, 1).*exp(-gpu_pl(p, 2:5)*transpose(gpu_a(:, :))) ), 1) / (sim_sum.each_photon_weight/part);
                    end
                end
            end
            
            % Take mean with each run
            ref_arr = sum(ref_all(:, :, :, 1:run), 4) / run;

            % Check CV
            CV_arr = std(ref_arr(:, :, NUM_SDS)) ./mean(ref_arr(:, :, NUM_SDS), 1); % only check last SDS
            CV = max(CV_arr);
            
            for k = 1:9 
                cv_record(k) = cv_record(k+1);
            end
            cv_record(10) = CV;
            if run > 10
                CV_UPDATED = cv_record(10) < max(cv_record(1:9));
            end                
            fprintf('    CV : %f\n',CV);
            
            % Save
            if CV < THRESHOLD_CV || run > THRESHOLD_RUN || CV_UPDATED == false
                if CV < THRESHOLD_CV;   fprintf('\tCV lower than 2%%!\n');  end
                if run > THRESHOLD_RUN;   fprintf('\tout of threshold !\n');  end
                if CV_UPDATED == false;   fprintf('\tCV not updated !\n');  end
                % Take mean with each part
                spec(id_thick, id_mus, :, :) = sum(ref_arr(:, :, :), 1) / part;
                for id_mua = 1:NUM_MUA
                    param_temp(1, 8:11)= a_arr(id_mua, :);
                    param = [param; param_temp];
                end
                save(['spec_' num2str(start_id) 'to' num2str(stop_id) '.mat'], 'spec');
                save(['para_' num2str(start_id) 'to' num2str(stop_id) '.mat'], 'param');
                save(fullfile(output_folder, ['thick_' num2str(id_thick)], ['mus_' num2str(id_mus)], 'cv.txt'), 'CV', '-ascii');
                NEXT_MUS = true;
            else
                run = run + 1;
                NEXT_MUS = false;
            end
        end
        time2 = toc;
    end
end

disp('Finished !')
