% Compare rmsp from 1000 random forward spectra, choose the better initial parameter for inverse fitting

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ChooseInitail.m
% Purpose: Compare rmsp from 1000 random forward spectra, choose the better
%          initial parameter for inverse fitting
% Author: Chiao-Yi Wang (NTU MD703)
%         Tzu-Chia Kao 
% Date: 20181117
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function ChooseInitial(target_name)
    global Spec initial_param wavelength_database rel_intensity sds_choose spec_target area_dect ADD_NOISE lambda NOISE_PATH spec_target_raw
    %% load file
    target = load(target_name);
    
%     spec_target_raw = target(:,2:end);
    target = [target(:,1) smoothdata(target(:,2:end), 'movmean', 3)];
%     target = [target(:,1) smoothdata(target(:,2), 'movmean', 7) smoothdata(target(:,3), 'movmean', 13) smoothdata(target(:,4), 'movmean', 3)];
%     target = [target(:,1) smoothdata(target(:,2:end), 'movmean', 25)];
%     target = [target(:,1) smoothdata(target(:,2:end), 'movmean', 21)];
%     fc = 200;
%     fs = 1000;
    
%     [b,a] = butter(2,fc/(fs/2));
%     target = [target(:,1) filter(b,a,target(:,2:end))]
%     target = [target(:,1) [filter(b,a,target(1:71,2:end)); target(72:end,2:end)]];
%     target = [target(:,1) [smoothdata(target(1:61,2:end), 'movmean', 25); target(62:end,2:end)]];
    target = [target(:,1) target(:,sds_choose+1)];
%     figure();
%     plot(target(:,1), target(:,2))
%      plot(target(:,1), target(:,3))
%       plot(target(:,1), target(:,4))

    spec_target_raw = target(:,2:end);
    %% compare all spec
    spec_target = interp1(target(:,1),target(:,2:end),lambda);
    
%     Spec = Spec(1:1000000, :, :);

    % gaussian noise
    if ADD_NOISE == true
        T_cv = readtable(NOISE_PATH);
        cv_wl = T_cv.wl;
        cv_ch1 = T_cv.ch1;
        cv_ch2 = T_cv.ch2;
        cv_ch3 = T_cv.ch3;
        cv_ch1 = interp1(cv_wl,cv_ch1,lambda);
        cv_ch2 = interp1(cv_wl,cv_ch2,lambda);
        cv_ch3 = interp1(cv_wl,cv_ch3,lambda);
        noiseSigma = [cv_ch1.*spec_target(:,1) cv_ch2.*spec_target(:,2) cv_ch3.*spec_target(:,3)];
        noise = noiseSigma .* randn(size(spec_target, 1), size(spec_target, 2));
        spec_target = spec_target + noise;
    end
    
    rmsp_all=zeros(size(Spec,1),1);
    
    for m = 1:size(Spec,1)
        data_temp = interp1(wavelength_database,squeeze(Spec(m, :, sds_choose)),lambda);
        de = (data_temp(:,1:end) - spec_target(:,1:end))./spec_target(:,1:end);     
        de2 = de.^2;
        rmsp = sqrt(mean(mean(de2)));
        rmsp_all(m,1) = rmsp;
    end

    [result,I] = sort(rmsp_all);
    Result = [I result initial_param(I,:)];
    Result = Result(1:20, :);
    save('RmspofForwardCompareResult.txt', 'Result', '-ascii');

    disp('    Compare to database Complete!');

end

