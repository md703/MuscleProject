% this can calculate predict and targer mu error

function error_rmse = errCalculate2(num_spec, PRED_FOLDER, TARGET_FOLDER)
% ############# Use min rmse as result #############
% Param define
% PRED_FOLDER = 'sds_2_5_8_11';
% TARGET_FOLDER = 'Target_Spec_20221021';
% num_spec = 50;
% num_x0 = 10;
num_wl = 22;
num_mu = 8;
num_abs = 16;
% offset = 10000;
wl = [700 708 716 724 732 739 745 752 759 769 779 788 798 805 812 820 826 832 840 854 866 880];
mu_predict = zeros(num_wl, num_mu);
mu_target = zeros(num_wl, num_mu);

%  mu error file name
csvfid_mae = 'all_mu_mae.csv';
csvfid_rmse = 'all_mu_rmse.csv';
header={'mua1', 'mus1', 'mua2', 'mus2', 'mua3', 'mus3', 'mua4', 'mus4', 'SPEC_RMSP'};
error_mae = zeros(num_spec, num_mu+1);
error_rmse = zeros(num_spec, num_mu+1);

%  abs error file name
csvfid_abserr = 'all_abs_err.csv';
header_abs = {'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'SPEC_RMSP'};
abs_error = zeros(num_spec, num_abs+1);

%  wl dependent error file name
csvfid_mua1 = 'all_mua1_err.csv';
csvfid_mus1 = 'all_mus1_err.csv';
csvfid_mua2 = 'all_mua2_err.csv';
csvfid_mus2 = 'all_mus2_err.csv';
csvfid_mua3 = 'all_mua3_err.csv';
csvfid_mus3 = 'all_mus3_err.csv';
csvfid_mua4 = 'all_mua4_err.csv';
csvfid_mus4 = 'all_mus4_err.csv';
header_wl = {'700' '708' '716' '724' '732' '739' '745' '752' '759' '769' '779' '788' '798' '805' '812' '820' '826' '832' '840' '854' '866' '880'};
mua1_error = zeros(num_spec, num_wl);
mus1_error = zeros(num_spec, num_wl);
mua2_error = zeros(num_spec, num_wl);
mus2_error = zeros(num_spec, num_wl);
mua3_error = zeros(num_spec, num_wl);
mus3_error = zeros(num_spec, num_wl);
mua4_error = zeros(num_spec, num_wl);
mus4_error = zeros(num_spec, num_wl);


for specID = 1 : num_spec
    temp_target = load(fullfile(TARGET_FOLDER, ['param_' num2str(specID) '.txt']));
    temp_target_abs = load(fullfile(TARGET_FOLDER, 'epsilon.txt'));
    mu_target = temp_target(:, 2:end);
    abs_target = temp_target_abs(specID, 2:end);
    SPEC_FOLDER = [PRED_FOLDER '/simspec_' num2str(specID) '_sds_7_9_12'];

    % find min rmsp index of initial value 
    fit_res = readtable(fullfile(SPEC_FOLDER, 'fit_res.csv'));
    fit_res_arr = table2array(fit_res);
    rmsp = fit_res_arr(:, end);
    [res, I] = sort(rmsp);
    
    % find mua, mus of rmsp min
    FIT_FOLDER = ['fit_all' num2str(I(1))];
    temp_pred = load(fullfile(SPEC_FOLDER, FIT_FOLDER, 'lsqMu_final.txt'));
    mu_predict = temp_pred(:, 2:end);
    
    % find abs of rmsp min
    abs_predict = fit_res_arr(I(1), 1:end-1);

    % calculate mu error
    error = abs((mu_predict - mu_target) ./ mu_target)*100;
    error_mae(specID, 1:end-1) = mean(abs(error), 1);
    error_rmse(specID, 1:end-1) = sqrt(mean(error.^2, 1));
    error_mae(specID, end) = rmsp(I(1));
    error_rmse(specID, end) = rmsp(I(1));
    mua1_error(specID, :) = error(:, 1)';
    mus1_error(specID, :) = error(:, 2)';
    mua2_error(specID, :) = error(:, 3)';
    mus2_error(specID, :) = error(:, 4)';
    mua3_error(specID, :) = error(:, 5)';
    mus3_error(specID, :) = error(:, 6)';
    mua4_error(specID, :) = error(:, 7)';
    mus4_error(specID, :) = error(:, 8)';

    % calculate abs error
    abs_error(specID, 1:end-1) = ((abs_predict - abs_target) ./ abs_target)*100;  
    abs_error(specID, end) = rmsp(I(1));
end

% delete outliers
error_mae = rmoutliers(error_mae);
error_rmse = rmoutliers(error_rmse);
abs_error = rmoutliers(abs_error);
mua1_error = rmoutliers(mua1_error);
mus1_error = rmoutliers(mus1_error);
mua2_error = rmoutliers(mua2_error);
mus2_error = rmoutliers(mus2_error);
mua3_error = rmoutliers(mua3_error);
mus3_error = rmoutliers(mus3_error);
mua4_error = rmoutliers(mua4_error);
mus4_error = rmoutliers(mus4_error);

% mua, mus table
table_mae = array2table(error_mae, 'VariableNames', header);
table_rmse = array2table(error_rmse, 'VariableNames', header);
% writetable(table_mae, csvfid_mae);
% writetable(table_rmse, csvfid_rmse);

% abs table
table_abs = array2table(abs_error, 'VariableNames', header_abs);
% writetable(table_abs, csvfid_abserr);

% wl dependent table
table_mua1 = array2table(mua1_error, 'VariableNames', header_wl);
table_mus1 = array2table(mus1_error, 'VariableNames', header_wl);
table_mua2 = array2table(mua2_error, 'VariableNames', header_wl);
table_mus2 = array2table(mus2_error, 'VariableNames', header_wl);
table_mua3 = array2table(mua3_error, 'VariableNames', header_wl);
table_mus3 = array2table(mus3_error, 'VariableNames', header_wl);
table_mua4 = array2table(mua4_error, 'VariableNames', header_wl);
table_mus4 = array2table(mus4_error, 'VariableNames', header_wl);
% writetable(table_mua1, csvfid_mua1);
% writetable(table_mus1, csvfid_mus1);
% writetable(table_mua2, csvfid_mua2);
% writetable(table_mus2, csvfid_mus2);
% writetable(table_mua3, csvfid_mua3);
% writetable(table_mus3, csvfid_mus3);
% writetable(table_mua4, csvfid_mua4);
% writetable(table_mus4, csvfid_mus4);



% Plot
% rmsePlot(error_rmse, 1);
% rmsePlot(error_rmse, 2);
% errwlPlot(wl, mua1_error, mua2_error, mua3_error, mua4_error, 1);
% errwlPlot(wl, mus1_error, mus2_error, mus3_error, mus4_error, 2);

end

% ###############################################################
% Plot
% error_rmse
function rmsePlot(error_rmse, mode)  % mua= 1 , mus=2
    figure();
    header1={'epidermis', 'dermis',  'fat', 'muscle'};
%     set(gca, 'position', [.17 .17 .80 .74] );   % 设置绘图框大小 [x-start, y-start, width, height]
%     set(gca,'Fontname','Times New Roman','Fontsize',13);  %设置图片中字体样式
    x_mean = mean(error_rmse(:, 1:end-1), 1);
    x_std = std(error_rmse(:, 1:end-1), 1);
    ya_mean = x_mean(:, [1 3 5 7]);
    ya_std = x_std(:, [1 3 5 7]);
    ys_mean = x_mean(:, [2 4 6 8]);
    ys_std = x_std(:, [2 4 6 8]);
    if mode == 1
        ym = ya_mean;
        ys = ya_std;
        yname = '\mu_a';
        name = 'mua_rmse.png';
    elseif mode == 2
        ym = ys_mean;
        ys = ys_std;
        yname = '\mu_s';
        name = 'mus_rmse.png';
    else
        disp('error !')
    end
    b = bar(ym, 0.5, 'FaceColor', 'flat');  % 绘制条形图，设置条形宽度 width = 0.5；修改条状颜色，灰色
    set(gca, 'xticklabels', header1, 'Fontname', 'Times New Roman', 'Fontsize',13); %修改横坐标轴标签及其文字样式
    yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]);
    ylim([0 100]);
    ytickformat('percentage');
    ylabel(yname);
    grid on
    hold on;  %在原图框上绘图，不再另起一个图框
    errorbar(ym, ys, 'black', 'Linestyle', 'None'); %添加误差棒，设置颜色，蓝色'b'
    hold off
    print(name,'-dpng','-r300')
%     saveas(gcf, name);
    close(gcf);
end

function errwlPlot(wl, err1, err2, err3, err4, mode) %1= mua, 2=mus
    figure();
    mu1_error_mean = mean(err1, 1);
    mu2_error_mean = mean(err2, 1);
    mu3_error_mean = mean(err3, 1);
    mu4_error_mean = mean(err4, 1);
    plot(wl, mu1_error_mean, 'o-', ...
        wl, mu2_error_mean, 's-', ...
        wl, mu3_error_mean, 'd-', ...
        wl, mu4_error_mean, '*-');
    % xticks(wl);
    yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]);
    ylim([0 100]);
    ytickformat('percentage');
    xlabel('Wavelength (nm)')
    if mode == 1
        ylabel('\mu_a');
        name = 'mua_wlerr.png';
    elseif mode == 2
        ylabel('\mu_s');
        name = 'mus_wlerr.png';
    else
        disp('Error !')
    end
    header1={'epidermis', 'dermis',  'fat', 'muscle'};
    legend(header1);
    print(name,'-dpng','-r300')
%     saveas(gcf, name);
    close(gcf);
end


