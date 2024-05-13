% this function can train ANN automatically with many newron number and SDS
% created by Tzu-Chia Kao 20181122
% edited by LEE, HAO-WEI 2022/9/22
clear; clc; close all;

%% param
MODE = 1; % 1: train deep network, 2: train shallow network
addThickness = true;
isLoading = true;
doRetrian = false;
testing_rate = 0.15;
val_rate = 0.1;
do_normalize = 1; % if =1, do normalization to spec and param
folder='20230918_all';
modelname = fullfile(folder, '5_neck_SDS_1-3.mat');

% neuron_number={[15 15] [25 25] [35 35] [45 45] [55 55] [65 65] [75 75] [85 85] [100 100]};
% neuron_number={[35 35] [45 45] [55 55] [65 65] [75 75] [85 85] [100 100] [150 150]};
% neuron_number={[200 200] [250 250] [300 200 100]};
% neuron_number={[550 350 150]};
% neuron_number={[550 550]};
% neuron_number={[850 550 300 150]};
% neuron_number={[150 150]};
% neuron_number={[1050 850 550 300]};
% neuron_number={[6000 3000 1500 500]};
% neuron_number={[1024 512 256 128]};
% neuron_number={[4096 2048 1024 512 256 128]};
% neuron_number={[8192 4096 2048 1024 512]};
% neuron_number={[4096 2048 1024 512]};
% neuron_number={[1024 1024 1024 1024 1024 1024 1024 1024]};
% neuron_number={[1024 1024 1024 1024 1024 1024]};
% neuron_number={[1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024 1024]};
% neuron_number={[100 300 800 500]};
neuron_number={[200 600 1600 1000]};
% neuron_number={[300 900 2400 1500]};
%% load file
% 
% parampath = [folder '/para_1to1.mat'];
% specpath = [folder '/spec_1to1.mat'];
% [param, spec] = arangeio(parampath, specpath);
% parampath = [folder '/para_1to343.mat'];
% specpath = [folder '/spec_1to343.mat'];
% [param, spec] = arangeio(parampath, specpath);
% parampath2 = [folder '/para_344to450.mat'];
% specpath2 = [folder '/spec_344to450.mat'];
% [param2, spec2] = arangeio(parampath2, specpath2);

parampath1 = [folder '/para_1to1_hw.mat'];
specpath1 = [folder '/spec_1to1_hw.mat'];
parampath2 = [folder '/para_1to1_by.mat'];
specpath2 = [folder '/spec_1to1_by.mat'];
parampath3 = [folder '/para_1to1_kb.mat'];
specpath3 = [folder '/spec_1to1_kb.mat'];
parampath4 = [folder '/para_1to1_syu.mat'];
specpath4 = [folder '/spec_1to1_syu.mat'];

% parampath2 = [folder '/para_60to90.mat'];
% specpath2 = [folder '/spec_60to90.mat'];
[param1, spec1] = arangeio(parampath1, specpath1);
[param2, spec2] = arangeio(parampath2, specpath2);
[param3, spec3] = arangeio(parampath3, specpath3);
[param4, spec4] = arangeio(parampath4, specpath4);
[param2, spec2] = arangeio(parampath2, specpath2);
param = [param1; param2; param3; param4];
spec = [spec1; spec2; spec3; spec4];
% spec = [spec(1:180000, :); spec2(180001:end, :)];
% % param = [param; param2;];
% spec = [spec(1350001:2379000, :); spec2(2379001:end, :)];
NUM_SDS = 3;

num_param = size(param, 1);

if ~addThickness
    IN_temp = param(:, 4:end);
else
    IN_temp = param;
end
Spec_temp = spec;

% random interpolate mua 3 10 10 10
% a = [100 150 100 45 0.0001 0.0001 0.0001 0.0001];
% b = [300 300 250 85 4      4       2       0.6];
% xq = (b-a).*rand(0.25*size(spec, 1), 1) + a;
% mus1 = [100 300]; mus2 = linspace(150, 300, 7);
% mus3 = linspace(100, 250, 4); mus4 = linspace(45, 85, 10);
% mua1 = linspace(0.0001, 4, 3); mua2 = linspace(0.0001, 4, 10);
% mua3 = linspace(0.0001, 2, 10); mua4 = linspace(0.0001, 0.6, 10);
% 
% vq_arr = zeros(0.25*size(spec, 1), size(spec, 2));
% for sds = 1:num_SDS
%     v = reshape(spec(:, sds), [10 10 10 3 10 4 7 2]);
%     v2 = permute(v, [8 7 6 5 4 3 2 1]);
%     vq = interpn(mus1, mus2, mus3, mus4, mua1, mua2, mua3, mua4, v2, xq(:, 1), xq(:, 2), xq(:, 3), xq(:, 4), xq(:, 5), xq(:, 6), xq(:, 7), xq(:, 8));
%     vq_arr(:, sds) = vq;
% end
% IN_temp = [IN_temp; xq];
% Spec_temp = [Spec_temp; vq_arr];
% 
clear('param', 'param2', 'spec', 'spec2', 'param', 'spec')


% random input output
IN = zeros(size(IN_temp));
rng = randperm(size(IN, 1));
IN = IN_temp(rng, :);
Spec = Spec_temp(rng, :);

clear('IN_temp', 'Spec_temp');

if do_normalize == 1
%     IN=normalize_param(IN,1);
    OUT = normalize_spec(Spec,1);
else
    OUT = Spec;
end

%% train deep network multi-output
if MODE == 1
    num_traindata = floor(size(IN,1)*(1-testing_rate-val_rate));
    num_valdata = floor(size(IN,1)*(val_rate));
    for N=1:size(neuron_number,2)
        disp(['training NN(' num2str(neuron_number{N}) ')']);
        output_folder=[datestr(now,'yyyy_mm_dd_HH_MM_SS') '_NN(' num2str(neuron_number{N}) ')'];
        mkdir(output_folder);
        test_error_record = []; % record the error
        neuron_num = neuron_number{N};
        if addThickness
            layers = [ ...
                featureInputLayer(11, 'Normalization', 'rescale-zero-one')
                fullyConnectedLayer(neuron_num(1))
                reluLayer
                fullyConnectedLayer(neuron_num(2))
                reluLayer
                fullyConnectedLayer(neuron_num(3))
                reluLayer
                fullyConnectedLayer(neuron_num(4))
                reluLayer
                sigmoidLayer
                fullyConnectedLayer(3)
                regressionLayer
            ];
        else
            layers = [ ...
                featureInputLayer(8, 'Normalization', 'rescale-zero-one')
                fullyConnectedLayer(neuron_num(1))
                reluLayer
                fullyConnectedLayer(neuron_num(2))
                reluLayer
                fullyConnectedLayer(neuron_num(3))
                reluLayer
                fullyConnectedLayer(neuron_num(4))
                reluLayer
                sigmoidLayer
                fullyConnectedLayer(3)
                regressionLayer
            ];
        end
        checkpointPath = output_folder;
        options = trainingOptions('adam', ...
            'ValidationData',{IN(num_traindata+1:num_traindata+num_valdata,:),OUT(num_traindata+1:num_traindata+num_valdata,:)}, ...
            'MiniBatchSize', 256, ...
            'MaxEpochs', 100, ...
            'Shuffle','every-epoch', ...
            'Plots','training-progress', ...
            'Verbose',false, ...
            'CheckpointPath',checkpointPath);
        setdemorandstream(391418381)
        % rand_seed=now;
        % setdemorandstream(rand_seed);
        % save(fullfile(output_folder,['rand_seed_' num2str(A) '.txt']),'rand_seed','-ascii');
        if isLoading
            net = load(modelname);
            net = net.net;
            if doRetrian
                [net, info] = trainNetwork(IN(1:num_traindata,:), OUT(1:num_traindata, :), net.Layers, options);
                fprintf('training rmse = %2.4f \n' , info.TrainingRMSE(end))
                currentfig = findall(groot, 'Tag', 'NNET_CNN_TRAININGPLOT_UIFIGURE');
                savefig(currentfig, [output_folder '/train_recoed' '.fig']);
                save([output_folder '/SDS_1-3'] ,'net')
            end
        else
            [net, info] = trainNetwork(IN(1:num_traindata,:), OUT(1:num_traindata, :), layers, options);
            fprintf('training rmse = %2.4f \n' , info.TrainingRMSE(end))
            currentfig = findall(groot, 'Tag', 'NNET_CNN_TRAININGPLOT_UIFIGURE');
            savefig(currentfig, [output_folder '/train_recoed' '.fig']);
            save([output_folder '/SDS_1-3'] ,'net')
    %     reflectance=predict(net, IN(num_traindata+num_valdata+1:end, :));
        end
        reflectance = zeros(size(Spec));
        num_batch = 1000;
        for batch = 1:floor(size(Spec, 1)/num_batch)
            p = (batch-1)*num_batch;
            reflectance(p+1:p+num_batch, :) = predict(net, IN(p+1:p+num_batch, :));
        end
        if do_normalize == 1
            reflectance = normalize_spec(reflectance,2);
        end
        train_err = reflectance(1:num_traindata, :)./Spec(1:num_traindata, :)-1;
        test_err = reflectance(num_traindata+num_valdata+1:end, :)./Spec(num_traindata+num_valdata+1:end, :)-1;
        train_error_mean=mean(abs(train_err));
        test_error_mean=mean(abs(test_err));
        train_error_std=std(train_err);
        test_error_std=std(test_err);
        train_error_rmse=sqrt(mean(train_err.^2));
        test_error_rmse=sqrt(mean(test_err.^2));
        
        for A = 1:NUM_SDS
            figure();
            plot(test_err(:, A));
            xlabel('testing data index');
            ylabel('Error');
            title(['SDS ' num2str(A) ' testing error']);
            saveas(gcf,[output_folder '/SDS_' num2str(A) '_testing_error.png']);
            figure();
            hist(test_err(:, A),50);
            xlabel('Error');
            ylabel('Count');
            title(['Ch ' num2str(A) ' testing error histogram']);
            saveas(gcf,[output_folder '/SDS_' num2str(A) '_testing_error_histogram.png']);
            fprintf(['SDS' num2str(A) ' : ']);
            fprintf('---- train error= %2.4f%%, rmse= %2.4f%%, std=%2.4f%%\n',train_error_mean(1, A)*100,train_error_rmse(1, A)*100,train_error_std(1, A)*100);
            fprintf('---- test error= %2.4f%%, rmse= %2.4f%%, std=%2.4f%%\n',test_error_mean(1, A)*100,test_error_rmse(1, A)*100,test_error_std(1, A)*100);
            
        end
        test_error_record=[test_error_mean' test_error_rmse' test_error_std'];
        test_error_record = double(test_error_record);
        save([output_folder '/test_error_record.txt'],'test_error_record','-ascii','-tabs');
        train_error_record=[train_error_mean' train_error_rmse' train_error_std'];
        train_error_record = double(train_error_record);
        save([output_folder '/train_error_record.txt'],'train_error_record','-ascii','-tabs');
        close all;
        fprintf('\n--------------------------\n\n')
    end
    
    disp('Done!');
end

%% train shallow Network
if MODE == 2
    ew = (1./OUT).^2;
    
    num_traindata=floor(size(IN,1)*(1-testing_rate));
    
    for N=1:size(neuron_number,2)
        disp(['training NN(' num2str(neuron_number{N}) ')']);
        output_folder=[datestr(now,'yyyy_mm_dd_HH_MM_SS') '_NN(' num2str(neuron_number{N}) ')'];
        mkdir(output_folder);
        test_error_record=[]; % record the error
        for A=1:NUM_SDS
            setdemorandstream(391418381)
            % rand_seed=now;
            % setdemorandstream(rand_seed);
            % save(fullfile(output_folder,['rand_seed_' num2str(A) '.txt']),'rand_seed','-ascii');
            disp(['-- training SDS' num2str(A)]);
    
            net = patternnet(neuron_number{N});
            net.divideFcn = 'divideblock';
            net.performFcn = 'mse';
            net.trainParam.max_fail = 2250;
            net.trainParam.epochs= 20000;
            [net,tr] = train(net,IN(1:num_traindata,:)',OUT(1:num_traindata,A)',{},{},ew(1:num_traindata,A)','useGPU','yes'); %'useParallel','yes'
            plotperform(tr);
            saveas(gcf,[output_folder '/train_recoed_SDS_' num2str(A) '.png']);
            close gcf;
            save([output_folder '/SDS_' num2str(A)],'net')
    
            reflectance=net(IN(num_traindata+1:end,:)');
            if do_normalize==1
                reflectance=normalize_spec(reflectance,2);
            end
            error=reflectance'./Spec(num_traindata+1:end,A)-1;
            error_mean=mean(abs(error));
            error_std=std(error);
            error_rmse=sqrt(mean(error.^2));
    
            figure();
            plot(error);
            xlabel('testing data index');
            ylabel('Error');
            title(['SDS ' num2str(A) ' testing error']);
            saveas(gcf,[output_folder '/SDS_' num2str(A) '_testing_error.png']);
            figure();
            hist(error,50);
            xlabel('Error');
            ylabel('testing data number');
            title(['SDS ' num2str(A) 'testing error histogram']);
            saveas(gcf,[output_folder '/SDS_' num2str(A) '_testing_error_histogram.png']);
            fprintf('---- error= %2.4f%%, rmse= %2.4f%%, std=%2.4f%%\n',error_mean*100,error_rmse*100,error_std*100);
            test_error_record=[test_error_record;error_mean error_rmse error_std];
        end
    
        save([output_folder '/error_record.txt'],'error_record','-ascii','-tabs');
        close all;
        fprintf('\n--------------------------\n\n')
    
    end
    
    disp('Done!');
end

% direction: if =1, normalize the input; if =2, denormalize the input
function output=normalize_spec(input,direction)
    if direction==1
        output=-log(input);
    elseif direction==2
%         output=power(10,-input);
        output=exp(-input);
    else
        assert(false,'Function ''normalize_spec'' param ''direction'' Error!');
    end
end

% normalize the parameters to [0,1]
% direction: if =1, normalize the input; if =2, denormalize the input
function output=normalize_param(input,direction)
    global folder;
    param_range=load([folder '/param_range.txt']);
    param_scaling=param_range(2,:)-param_range(1,:);
    if direction==1
        output=(input-param_range(1,:))./param_scaling;
    elseif direction==2
        output=input.*param_scaling+param_range(1,:);
    else
        assert(false,'Function ''normalize_spec'' param ''direction'' Error!');
    end
end

function [param, spec] = arangeio(parampath, specpath)
    param_file = load(parampath);
    spec_file = load(specpath);
    param = param_file.param;
    
    NUM_THICK = size(spec_file.spec, 1);
    NUM_MUS = size(spec_file.spec, 2);
    NUM_MUA = size(spec_file.spec, 3);
    NUM_SDS = size(spec_file.spec, 4);
    spec = zeros(NUM_THICK*NUM_MUS*NUM_MUA, NUM_SDS);

    % Squeeze spec dim
    for i = 1:NUM_THICK
        for j = 1:NUM_MUS 
            for k = 1:NUM_MUA
                p = (i-1) * NUM_MUS * NUM_MUA + (j-1) * NUM_MUA + k;
                spec(p, :) = spec_file.spec(i, j, k, :);
            end
        end
    end
end

