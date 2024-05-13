% this can calculate compare target and fit spectrum
%% 
clc; clear; close all;

%% Param define

sds_choose = [2 5 8 11];
PRED_FOLDER = 'sds_2_5_8_11';
TARGET_FOLDER = 'Target_Spec_20220920';
num_spec = 50;
num_x0 = 10;
num_wl = 22;
num_mu = 8;
num_abs = 16;
offset = 10000;
wl = [700 708 716 724 732 739 745 752 759 769 779 788 798 805 812 820 826 832 840 854 866 880];
rmsp_arr = zeros(num_spec, 4);
mu_predict = zeros(num_wl, num_mu);
mu_target = zeros(num_wl, num_mu);

% load Forward model
ann_path=fullfile('data', 'ANN_model', 'SDS_1-12.mat');
load(ann_path, 'net');

% Make folder to save figure
OUT_FOLDER = 'Compare_fig';
mkdir(OUT_FOLDER);

for specID = 1 : num_spec
    SPEC_FOLDER = ['simspec_' num2str(specID+offset) '_' PRED_FOLDER];
    % find min rmsp index of initial value 
    fit_res = readtable(fullfile(SPEC_FOLDER, 'fit_res.csv'));
    fit_res_arr = table2array(fit_res);
    rmsp = fit_res_arr(:, end);
    [res, I] = sort(rmsp);
    
    % find mua, mus of rmsp min
    FIT_FOLDER = ['fit_all' num2str(I(1))];
    TRUE_MU_NAME = ['param_' num2str(specID+offset) '.txt'];
    temp_mu = load(fullfile(TARGET_FOLDER, TRUE_MU_NAME));
    temp_target = load(fullfile(SPEC_FOLDER, FIT_FOLDER, 'lsqSpec_target.txt'));
    target_spec = temp_target(:, sds_choose+1);
    target_mu = temp_mu(:, [3 5 7 9 2 4 6 8]);
    fit_spec = ANN_predict_matlab(target_mu, sds_choose, net);
    fit_spec = fit_spec(:, sds_choose);

    % RMSP fix 4 sds
    de = (fit_spec-target_spec)./target_spec;
    de2 = de.^2;
    rmsp = sqrt(mean(de2, 1))*100;
    rmsp_arr(specID, :) = rmsp;

    % plot
    figure('Position',[0,50,1920,950]);
    

    % SDS 1
    subplot(1, 4, 1);
    hold on
    plot(wl, fit_spec(:, 1));
    plot(wl, target_spec(:, 1));
    xlabel("Wavelength (nm)");
    ylabel('Reflectance');
    legend('target ANN', 'target Truth');
    ylim = ([1.1e-5 1.3e-5]);
    rmsp_str = sprintf('RMSP = %5.2f%%', rmsp(1));
    title(rmsp_str);
    hold off

    % SDS 2
    subplot(1, 4, 2);
    hold on
    plot(wl, fit_spec(:, 2));
    plot(wl, target_spec(:, 2));
    xlabel("Wavelength (nm)");
    ylabel('Reflectance');
    legend('target ANN', 'target Truth');
    ylim = ([2e-7 3e-6]);
    rmsp_str = sprintf('RMSP = %5.2f%%', rmsp(2));
    title(rmsp_str);
    hold off

    % SDS 3
    subplot(1, 4, 3);
    hold on
    plot(wl, fit_spec(:, 3));
    plot(wl, target_spec(:, 3));
    xlabel("Wavelength (nm)");
    ylabel('Reflectance');
    legend('target ANN', 'target Truth');
    ylim = ([7e-10 6e-8]);
    rmsp_str = sprintf('RMSP = %5.2f%%', rmsp(3));
    title(rmsp_str);
    hold off

    % SDS 4
    subplot(1, 4, 4);
    hold on
    plot(wl, fit_spec(:, 4));
    plot(wl, target_spec(:, 4));
    xlabel("Wavelength (nm)");
    ylabel('Reflectance');
    legend('target ANN', 'target Truth');
    ylim = ([5e-10 5e-8]);
    rmsp_str = sprintf('RMSP = %5.2f%%', rmsp(4));
    title(rmsp_str);
    hold off

%     title(num2str(specID));
%     annotation('textbox', [0.47, 0.95, 0.1, 0.05], 'string', rmsp_str, 'FontSize', 18)
%     t.FontSize = 12;
%     text(1, 1, rmsp_str);
    FIG_NAME = sprintf('%03d.png', specID);
    saveas(gcf, fullfile(OUT_FOLDER, FIG_NAME));
    close(gcf);
end

header={'SDS1', 'SDS2', 'SDS3', 'SDS4'};
rmsp_table = array2table(rmsp_arr,'VariableNames', header);
% writetable(rmsp_table, fullfile(OUT_FOLDER, 'rmsp.csv'))

% ###############################################################
