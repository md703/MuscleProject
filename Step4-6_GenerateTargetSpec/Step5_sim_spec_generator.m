%%  run mc simulated and database spectrum
%  2022/6/14 by LEE, HAO-WEI
clc; clear; close all;

% setting
mode = 1; %1= wmc, 2= normal, 3= ANN
start_id = 1;
stop_id = 2;

input_folder = 'Target_Spec_20230416';
sim_set = jsondecode(fileread('sim_setup.json')); 
wl = load('2023_0422_1523_wl.txt');
feps = load(fullfile(input_folder, 'epsilon.txt')); 
num_wl = size(wl, 2);
num_sds = sim_set.probes.num_SDS;

output_folder = fullfile(input_folder, 'wmc');
if ~exist(output_folder, 'dir')
    mkdir(output_folder)
end

tic; time1 = toc;
%%
for i = start_id:stop_id
    if i == start_id disp('Start !');end
    time2 = toc;
    fid = load(fullfile(input_folder, ['param_' num2str(i) '.txt']));
    wl = fid(:, 1);
    mus1 = fid(:, 2);
    mus2 = fid(:, 3);
    mus3 = fid(:, 4);
    mus4 = fid(:, 5);
    mua1 = fid(:, 6);
    mua2 = fid(:, 7);
    mua3 = fid(:, 8);
    mua4 = fid(:, 9);
    th1 = feps(i, 2);
    th2 = feps(i, 3);
    th3 = feps(i, 4);
    n1 = 1.400;
    n2 = 1.400;
    n3 = 1.400;
    n4 = 1.400;
    g1 = 0.8040;
    g2 = 0.7150;
    g3 = 0.9000;
    g4 = 0.9300;

    if mode == 1
        spec = zeros(size(wl, 1), num_sds);
        for j = 1:size(wl, 1)
            param = [th1 0 mus1(j) n1 g1 th2 0 mus2(j) n2 g2 th3 0 mus3(j) n3 g3 0 mus4(j) n4 g4];
            save('GPUMC_input.txt', 'param', '-ascii');
            delete('summary.json', 'pathlength_SDS_*');
            if ispc
                command = ['MCML_GPU.exe sim_setup.json GPUMC_input.txt ' output_folder '/simspec_' num2str(i) '.txt' ' -R -P -B'];
                [~,~] = system(command);
            elseif isunix
                command = ['MCML_GPU sim_setup.json GPUMC_input.txt ' output_folder '/simspec_' num2str(i) '.txt' ' -R -P -B'];
                [~,~] = system(command);
            else
                disp('Platform not supported')
                exit
            end
            a_arr = [mua1(j) mua2(j) mua3(j) mua4(j)];
            ref = [];
            sim_sum = jsondecode(fileread('summary.json')); % if json allready exist, will crash
            for s = 1:num_sds
                PL{s} = load_binary_pathlength_output('summary.json',s, ['pathlength_SDS_' num2str(s) '.bin']);
                out = sum(PL{s}(:, 1).*exp(-PL{s}(:, 2:5)*transpose(a_arr)), 1) / sim_sum.each_photon_weight;
                ref = [ref out];
            end
            spec(j, :) = ref;
            delete('summary.json', 'pathlength_SDS_*');
        end

    elseif mode == 2
        for j = 1:size(wl, 1)
            param = [th1 mua1(j) mus1(j) n1 g1 th2 mua2(j) mus2(j) n2 g2 th3 mua3(j) mus3(j) n3 g3 mua4(j) mus4(j) n4 g4];
            save('GPUMC_input.txt', 'param', '-ascii');
            if ispc
                command = ['MCML_GPU.exe simulated_spec.json GPUMC_input.txt sim_spec/wmc/simspec_' num2str(i) '.txt'];
                system(command);
            elseif isunix
                command = ['MCML_GPU simulated_spec.json GPUMC_input.txt sim_spec/wmc/simspec_' num2str(i) '.txt'];
                system(command);
            else
                disp('Platform not supported')
                exit
            end
        end
        spec = load(['sim_spec/wmc/simspec_' num2str(i) '.txt']);
    else disp('This mode not found !'); exit;
    end
    time3 = toc - time2;
    disp(['Total count = ' num2str(time3) ' s'])
    fprintf('Run spectrum %5d / %5d\n', i, stop_id);
    spec = [wl spec];
    save(fullfile(output_folder,  ['simspec_' num2str(i) '.txt']), 'spec', '-ascii');
end

disp('Finished !')

%% test epi
% num_set = 10;
% mus = [100 150 200 250 300];
% for i = 1:num_set
%     for k = 1:5
%         fid = load(['test_epi/set_' num2str(i) '/mus_' num2str(mus(k)) '.txt']);      
%         wl = fid(:, 1);
%         mua1 = fid(:, 2);
%         mus1 = fid(:, 3);
%         mua2 = fid(:, 4);
%         mus2 = fid(:, 5);
%         mua3 = fid(:, 6);
%         mus3 = fid(:, 7);
%         mua4 = fid(:, 8);
%         mus4 = fid(:, 9);
%         th1 = 0.0100;
%         th2 = 0.2000;
%         th3 = 0.1000;
%         n1 = 1.4300;
%         n2 = 1.4300;
%         n3 = 1.4400;
%         n4 = 1.3800;
%         g1 = 0.8040;
%         g2 = 0.7150;
%         g3 = 0.9000;
%         g4 = 0.9300;
%     
%         time2 = toc;
%         if mode == 1
%             spec = zeros(size(wl, 1), num_sds);
%             for j = 1:size(wl, 1)
%                 param = [th1 0 mus1(j) n1 g1 th2 0 mus2(j) n2 g2 th3 0 mus3(j) n3 g3 0 mus4(j) n4 g4];
%                 %         param = [th1 0 300 n1 g1 th2 0 150 n2 g2 th3 0 100 n3 g3 0 45 n4 g4];
%                 save('GPUMC_input.txt', 'param', '-ascii');
%                 command = ['MCML_GPU.exe simulated_spec.json GPUMC_input.txt test_epi/set_' num2str(i) '/spec_' num2str(mus(k)) '.txt -R -P -B'];
%                 [~,~] = system(command);
%                 a_arr = [mua1(j) mua2(j) mua3(j) mua4(j)];
%                 %         a_arr = [0.0001 0.0001 0.44452222 0.26672222];
%                 ref = [];
%                 for s = 1:num_sds
%                     PL{s} = load_binary_pathlength_output('summary.json',s, ['pathlength_SDS_' num2str(s) '.bin']);
%                     out = sum(PL{s}(:, 1).*exp(-PL{s}(:, 2:5)*transpose(a_arr)), 1) / 4.29497e+17; %1e8
%                     ref = [ref out];
%                 end
%                 spec(j, :) = ref;
%                 delete('summary.json', 'pathlength_SDS_*');
%             end
%     
%         elseif mode == 2
%             for j = 1:size(wl, 1)
%                 param = [th1 mua1(j) mus1(j) n1 g1 th2 mua2(j) mus2(j) n2 g2 th3 mua3(j) mus3(j) n3 g3 mua4(j) mus4(j) n4 g4];
%                 %         param = [th1 0 300 n1 g1 th2 0 150 n2 g2 th3 0 100 n3 g3 0 45 n4 g4];
%                 save('GPUMC_input.txt', 'param', '-ascii');
%                 command = ['MCML_GPU.exe simulated_spec.json GPUMC_input.txt sim_spec/wmc/simspec_' num2str(i) '.txt'];
%                 system(command);
%             end
%             spec = load(['sim_spec/wmc/simspec_' num2str(i) '.txt']);
%     
%         elseif mode == 3      
%             param = [mus1 mus2 mus3 mus4 mua1 mua2 mua3 mua4];
%             spec = double(predict(net, param));
%             spec = power(10, -spec);
%         end
%         time3 = toc - time2;
%         disp(['Total count = ' num2str(time3) ' s'])
%         
%         spec = [wl spec];
%         save(['test_epi/set_' num2str(i) '/spec_' num2str(mus(k)) '.txt'], 'spec', '-ascii');
%     end
% end