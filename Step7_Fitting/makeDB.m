%% make DataBase
global lambda sds_choose SDS_Set 
a= load('data/20180524_database.mat','wavelength_database');
lambda=a.wavelength_database;
sds_choose = [1 2 3];
          %up-a1    up-k1    hc      sto2    bt-a     bt-k     th1     mel   
        
Lbound =   [3000     1     0.000    0.01    3000       1     0.001    0.01 ...
           %up-a2  up-k2   bt-a2  bt-k2 th2   met  biliverdin    bilirubin
             30     0.1    30     0.1  0.001   0     0           0];
Ubound =   [25000    3     0.005     1      25000      3     0.006    0.15 ...   
             500     0.6    500    0.6  0.006 0.2 0.2 0.2];
initial_param=[];
Mu={};
Spec={};
all_num=100000;
    mua_up = load('data/epsilon/epsilon_2.txt');             % mua of upper layer

for number=1:all_num
    fprintf('%d/%d ( %f %%) \n',number,all_num,(number/all_num)*100)
    while 1
    rng('shuffle')
    
    %up-a1    up-k1    hc      sto2    bt-a     bt-k     th1     mel 
    %up-a2  up-k2   bt-a2  bt-k2 th2   met  biliverdin    bilirubin
    upa1=(25000-3000)*rand+3000;
    hc=(0.003-0.001)*rand+0.001;
    upk1=(2.5-1.5)*rand+1.5;upk2=(0.4-0.3)*rand+0.3;upa2=(375-130)*rand+130;sto2=(1-0.01)*rand+0.01;
    bta=(18000-7000)*rand+7000;bta2=(375-130)*rand+130;btk=(2.5-1.5)*rand+1.5;btk2=(0.4-0.25)*rand+0.25;
    th1=(0.01-0.001)*rand+0.001;th2=(0.01-0.001)*rand+0.001;
    mel=(0.01)*rand+0.01;biliverdin=0.00001*rand;bilirubin=0.00001*rand;met=0.00001*rand;

    para=[upa1 upk1 hc sto2 bta btk th1 mel upa2 upk2 bta2 btk2 th2...
        met biliverdin bilirubin];
    mu = Mu_generator(para);
    layer_thickness1 = ones(size(lambda))*para(7);
    layer_thickness2 = ones(size(lambda))*para(13);
     %paramSet=[th1             mua1     th2              mua2    mus2    mua3    mus3];
    %mus1=mus2
    paramSet=[layer_thickness1 mu(:,1)  layer_thickness2 mu(:,3) mu(:,4) mu(:,5) mu(:,6)];
    %out of ann range
     if paramSet(1,2)<5&&paramSet(end,2)>0.1&&paramSet(end,4)>1&&paramSet(1,4)<350....
                &&paramSet(end,5)>10&&paramSet(1,5)<700&&paramSet(end,6)>0.01&&paramSet(1,6)<16&&....
                paramSet(end,7)>10&&paramSet(1,7)<500
                break
     end
%         fprintf('out of ann range\n')
    end
    spec=[];
    for i=1:2
        SDS_Set=i;        
    spec_tmp=ANN_predict_matlab(paramSet,sds_choose);
    spec=[spec spec_tmp];
    end
    initial_param=[initial_param;para];
    Mu={Mu{:} paramSet};
    Spec={Spec{:} spec};
    fprintf('make a spec\n')

end
wavelength_database=lambda;
save('data/20210809_database.mat','Spec','initial_param','wavelength_database','Mu')
disp('Done')
function [mu] = Mu_generator(para)
    global lambda;global tissue_type;
    
    tissue_type=1;
    %% Data import
    mua_up = load('data/epsilon/epsilon_2.txt');             % mua of upper layer
    epsilon_hb = load('data/epsilon/epsilon.txt');           % mua of hb
    mua_colla = load('data/epsilon/collagen_mua_data.txt');  % mua of collagen
    mua_water = load('data/epsilon/water_mua.txt');          % mua of water
    mua_mel = load('data/epsilon/mel_mua.txt');              %Wang modified
    if tissue_type==1
    mua_metHb = load('data/epsilon/methemoglobin_extinction_Extrapolate.txt');
    mua_biliverdin = load('data/epsilon/biliverdin_dimethyl_ester_extinction.txt');
    mua_bilirubin = load('data/epsilon/bilirubin_extinction.txt');
    
    %% absorption spectra \ volume fraction
    
    vol_met=para(14);
    vol_biliverdin=para(15);
    vol_bilirubin=para(16);    
    vol_hc = para(3);                   
    vol_water = 0.7;
    vol_colla = 1-vol_water-vol_hc-vol_met-vol_biliverdin-vol_bilirubin;
    else
    vol_hc = para(3);                   
    vol_water = 0.7;
    vol_colla = 1-vol_water-vol_hc;
    end
    mel = para(8);
    sto2 = para(4);
    


    % mua upper layer
    ua_up = interp1(mua_up(:,1),mua_up(:,2),lambda(:,1)); 
    % mua hb1 hb2
    temp_hb1 = interp1(epsilon_hb(:,1),epsilon_hb(:,2),lambda(:,1));
    temp_hb2 = interp1(epsilon_hb(:,1),epsilon_hb(:,3),lambda(:,1));
    ua_hc = ( (sto2*2.303.*temp_hb1/64535)+((1-sto2)*2.303*temp_hb2/64500) )*150;
    % mua water
    ua_water = interp1(mua_water(:,1),mua_water(:,2),lambda(:,1));
    % mua collagen
    ua_colla = interp1(mua_colla(:,1),mua_colla(:,2),lambda(:,1));
    %mua mel %%Wang modified
    ua_mel = interp1(mua_mel(:,1),mua_mel(:,2),lambda(:,1));
    if tissue_type==1
    %mua MetHb
    ua_MetHb=interp1(mua_metHb(:,1),mua_metHb(:,2),lambda(:,1));
    %mua biliverdin
    ua_biliverdin=interp1(mua_biliverdin(:,1),mua_biliverdin(:,2),lambda(:,1));
    %mua bilirubin
    ua_bilirubin=interp1(mua_bilirubin(:,1),mua_bilirubin(:,2),lambda(:,1));
    end
    %% Wavelength-dependent function
    
    epi1_g=0.835;
    epi2_g=0.75;
    der_g=0.715;
    
    %%% ua1 & us1
    up_a1 = ua_up;
    %up_s1 = 1.3*((para(1)*1000*lambda.^-para(2) + para(9)*lambda.^-para(10))./(1 - epi1_g));

    %%% ua2 & us2
    up_a2 = ua_up*(1-mel) + mel*ua_mel;
    up_s2 =  ((para(1)*1000*lambda.^-para(2) + para(9)*lambda.^-para(10))./(1 - epi2_g));
    up_s1 = up_s2*1.3;

    %%% ua3 & us3
    if tissue_type==1
        bt_a = vol_hc*ua_hc + vol_colla*ua_colla + vol_water*ua_water+ua_MetHb*vol_met+ua_biliverdin*vol_biliverdin+ua_bilirubin*vol_bilirubin;  
    else
        bt_a = vol_hc*ua_hc + vol_colla*ua_colla + vol_water*ua_water;
    end
    bt_s = (para(5)*1000*lambda.^-para(6) + para (11)*lambda.^-para(12))./(1-der_g);

    mu = [up_a1 up_s1 up_a2 up_s2 bt_a bt_s];
end