%%
clc; clear; close all;

num_spec = 3;
num_sds = 12;

load('fitting_program\data\ANN_model\SDS_1-12.mat', 'net');
th1 = 0.0100;
th2 = 0.2000;
th3 = 0.1000;
n1 = 1.4300;
n2 = 1.4300;
n3 = 1.4400;
n4 = 1.3800;
g1 = 0.8040;
g2 = 0.7150;
g3 = 0.9000;
g4 = 0.9300;

for i = 1:num_spec
    if ~exist(['test_ANN/spec_' num2str(i)'])
        mkdir(['test_ANN/spec_' num2str(i)'])
    end
    fid = load(['sim_spec/param_' num2str(i) '.txt']);    
    wl = fid(:, 1);
    mua1 = fid(:, 2);
    mus1 = fid(:, 3);
    mua2 = fid(:, 4);
    mus2 = fid(:, 5);
    mua3 = fid(:, 6);
    mus3 = fid(:, 7);
    mua4 = fid(:, 8);
    mus4 = fid(:, 9);
    spec = [];
    time2 = toc;
    for j = 1:size(wl, 1)
        param = [mus1(j) mus2(j) mus3(j) mus4(j) mua1(j) mua2(j)  mua3(j)  mua4(j) ];
        spec = [spec; predict(net, param);];
    end
    spec=power(10,-spec);
    time3 = toc - time2;
    disp(['Total count = ' num2str(time3) ' s'])
    
    spec = [wl spec];
    fid2 = load(['sim_spec/wmc/simspec_' num2str(i) '.txt']);
    
    error = (spec(:, 2:end) - fid2(:, 2:end)) ./fid2(:, 2:end);
    error_mean1 = mean(abs(error));
    error_std = std(error);
    error_2 = error.^2;
    error_mean = mean(error_2);
    error_rmse = sqrt(error_mean);
    for j = 1:size(error, 2)
        fprintf('%d  ---- error= %2.4f%%, rmse= %2.4f%%, std=%2.4f%%\n',j,error_mean1(j)*100,error_rmse(j)*100,error_std(j)*100);
        plot(fid2(:, 1), fid2(:, j+1));
        hold on
        plot(spec(:, 1), spec(:, j+1));
        hold off
        xlabel('wavelength(nm)');
        ylabel('reflectance');
        title(['SDS = ' num2str(j) ' mm']);
        legend({'target' 'ANN'},'location','Best');
        saveas(gcf,['test_ANN/spec_' num2str(i) '/sds_' num2str(j) '.png']);
        close(gcf);
    end
    spec = double(spec);
    save(['sim_spec/predict/' num2str(i) '.txt'], 'spec', '-ascii');
    
end
    