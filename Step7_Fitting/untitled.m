clc; clear; close all
pred_folder1 = 'sds_7_9_12_1';
pred_folder2 = 'sds_7_9_12_2';
tar_folder = 'Target_Spec_20221021';

err1 =  errCalculate2(50, pred_folder1, tar_folder);
err2 =  errCalculate2(50, pred_folder2, tar_folder);
rmsePlot2(err1,err2, 1);
rmsePlot2(err1,err2, 2);


function rmsePlot2(err1,err2,  mode)  % mua= 1 , mus=2
    figure();
    header1={'epidermis', 'dermis',  'fat', 'muscle'};
    %     set(gca, 'position', [.17 .17 .80 .74] );   % 设置绘图框大小 [x-start, y-start, width, height]
    %     set(gca,'Fontname','Times New Roman','Fontsize',13);  %设置图片中字体样式
    x1_mean = mean(err1(:, 1:end-1), 1);
    x1_std = std(err1(:, 1:end-1), 1);
    ya1_mean = x1_mean(:, [1 3 5 7]);
    ya1_std = x1_std(:, [1 3 5 7]);
    ys1_mean = x1_mean(:, [2 4 6 8]);
    ys1_std = x1_std(:, [2 4 6 8]);
    
    x2_mean = mean(err2(:, 1:end-1), 1);
    x2_std = std(err2(:, 1:end-1), 1);
    ya2_mean = x2_mean(:, [1 3 5 7]);
    ya2_std = x2_std(:, [1 3 5 7]);
    ys2_mean = x2_mean(:, [2 4 6 8]);
    ys2_std = x2_std(:, [2 4 6 8]);
    
    if mode == 1
        ym1 = ya1_mean;
        ys1 = ya1_std;
        yname = '\mu_a';
        name = 'mua_rmse.png';
        ym2 = ya2_mean;
        ys2 = ya2_std;
        ys = [ys1(1) ys2(1); ys1(2) ys2(2); ys1(3) ys2(3); ys1(4) ys2(4) ];

    elseif mode == 2
        ym1 = ys1_mean;
        ys1 = ys1_std;
        yname = '\mu_s';
        name = 'mus_rmse.png';
        ym2 = ys2_mean;
        ys2 = ys2_std;
        ys = [ys1(1) ys2(1); ys1(2) ys2(2); ys1(3) ys2(3); ys1(4) ys2(4) ];
    else
        disp('error !')
    end
    ym = [ym1(1) ym2(1); ym1(2) ym2(2); ym1(3) ym2(3); ym1(4) ym2(4) ];

    b = bar(ym, 0.5, 'FaceColor', 'flat');  % 绘制条形图，设置条形宽度 width = 0.5；修改条状颜色，灰色
    set(gca, 'xticklabels', header1, 'Fontname', 'Times New Roman', 'Fontsize',13); %修改横坐标轴标签及其文字样式

    % This will produce 4 groups of 3 different colored bars
    % set 3 display names for the 3 handles
%     set(b, {'DisplayName'}, {'with noise','without noise'}')
    % Legend will show names for each color
    

    yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]);
    ylim([0 100]);
    ytickformat('percentage');
    ylabel(yname);
    grid on
    hold on;  %在原图框上绘图，不再另起一个图框

    % Example data 
%     model_series = [10 40 50 60; 20 50 60 70; 30 60 80 90]; 
%     model_error = [1 4 8 6; 2 5 9 12; 3 6 10 13]; 
%     b = bar(ym, 'grouped');
%     hold on
    % Calculate the number of groups and number of bars in each group
    [ngroups,nbars] = size(ym);
    % Get the x coordinate of the bars
    x = nan(nbars, ngroups);
    for i = 1:nbars
        x(i,:) = b(i).XEndPoints;
    end
    % Plot the errorbars
    errorbar(x',ym,ys,'k','linestyle','none');
    hold off
    legend('with noise','without noise');


%     errorbar(ym, ys, 'black', 'Linestyle', 'None'); %添加误差棒，设置颜色，蓝色'b'
%     hold off
    print(name,'-dpng','-r300')
    %     saveas(gcf, name);
    close(gcf);
end