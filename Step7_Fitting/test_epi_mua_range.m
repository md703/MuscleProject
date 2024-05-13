% This code can plot target spectrum mua/mus range
clc; clear; close all;

%% mua range
folder = 'Target_Spec_20221021';
para = zeros(50, 22, 9);
for i = 1:50
    fid = [folder '/param_' num2str(i) '.txt'];
    ftemp = load(fid);
    para(i, :, :) = ftemp;
end

wl = para(1, :, 1);
epi = para(:, :, 2);
figure();
for i = 1:50
    plot(wl, epi(i, :));
    title('50 epidermis \mu_a of target spectrum');
    xlabel('Wavelength (nm)');
    ylabel('Absorption coefficient (cm^-^1)')
    hold on
end
hold off
saveas(gcf, 'test_epi/epi_range.png')

%%
% load Forward model
ann_path=fullfile('data', 'ANN_model', 'SDS_1-12.mat');
load(ann_path, 'net');

%%
folder = 'Target_Spec_20221021';
mu = load([folder '/param_2.txt']);
wl = mu(:, 1);
epi = mu(:, 2);

mu_p10 = epi.*1.1;
mu_p20 = epi.*1.2;
mu_p30 = epi.*1.3;
mu_n10 = epi.*0.9;
mu_n20 = epi.*0.8;
mu_n30 = epi.*0.7;
figure();
plot(wl, epi, ...
    wl, mu_p10, ...
    wl, mu_p20, ...
    wl, mu_p30, ...
    wl, mu_n10, ...
    wl, mu_n20, ...
    wl, mu_n30);
xlabel('Wavelength (nm)');
ylabel('Absorption coefficient (cm^-^1)');
title('Target 2');
label = {'Origin', '+10%', '+20%', '+30%', '-10%', '-20%', '-30%'};
legend(label);
% saveas(gcf, 'test_epi/epi_range1.png')

%%
sds_choose = [6 9 12];
mu_epi = [epi mu_p10 mu_p20 mu_p30 mu_n10 mu_n20 mu_n30];
figure('Renderer', 'painters', 'Position', [10 10 1280 720])

% for i = 1:7
%     paramSet = [mu(:, 3) mu(:, 5) mu(:, 7) mu(:, 9) mu_epi(:, i) mu(:, 4) mu(:, 6) mu(:, 8)];
%     spec = ANN_predict_matlab(paramSet, sds_choose, net); % use ANN to predict spectrum
%     spec = spec(:, sds_choose);   
%     for sds = 1:3
%         subplot(1, 3, sds);
%         plot(wl, spec(:,sds), ...
%             wl, spec(:,sds), ...
%             wl, spec(:,sds), ...
%             wl, spec(:,sds), ...
%             wl, spec(:,sds), ...
%             wl, spec(:,sds), ...
%             wl, spec(:,sds));        
%     end
%     hold on
% end
sds_name = {'SDS = 4 mm', 'SDS = 7 mm', 'SDS = 10 mm'};
for sds = 1:3
    subplot(1, 3, sds);
    for i = 1:7
        paramSet = [mu(:, 3) mu(:, 5) mu(:, 7) mu(:, 9) mu_epi(:, i) mu(:, 4) mu(:, 6) mu(:, 8)];
        spec = ANN_predict_matlab(paramSet, sds_choose, net); % use ANN to predict spectrum
        spec = spec(:, sds_choose);   
        plot(wl, spec(:,sds), ...
            wl, spec(:,sds), ...
            wl, spec(:,sds), ...
            wl, spec(:,sds), ...
            wl, spec(:,sds), ...
            wl, spec(:,sds), ...
            wl, spec(:,sds));   
        hold on
    end
    title(sds_name{sds});
    xlabel('Wavelength (nm)');
    ylabel('Reflectance');
    label = {'Origin', '+10%', '+20%', '+30%', '-10%', '-20%', '-30%'};
    legend(label, 'Location','bestoutside');
end

sgtitle('Target 2');

hold off
label = {'Origin', '+10%', '+20%', '+30%', '-10%', '-20%', '-30%'};
legend(label);
saveas(gcf, 'test_epi/epi_spec2.png')
