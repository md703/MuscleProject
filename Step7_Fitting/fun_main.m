% this function can fitting spec automatically

function fun_main(target_spec,target_name, OUTPUT_FOLDER_NAME)
    global sds_choose num_init
       
    %% param
    % output_folder=[datestr(now,'yyyy_mm_dd_HH_MM_SS') '_' target_name '_set_' num2str(SDS_Set) '_Choose_' num2str(sds_choose)];
    sds_str = strjoin(string(sds_choose), '_');
    OUTPUT_FOLDER = fullfile(OUTPUT_FOLDER_NAME, convertStringsToChars(string(target_name) +  "_sds_" + sds_str));    
    
    %% initialize
    if exist(OUTPUT_FOLDER) 
        rmdir(OUTPUT_FOLDER, 's');
    end
    while ~mkdir(OUTPUT_FOLDER) 
        disp(['Cannot make ' OUTPUT_FOLDER ' !'])
        pause(0.5)
    end;
    while ~mkdir(fullfile(OUTPUT_FOLDER, 'spec_pics')); % to store the spec pictures
        disp(['Cannot make ' fullfile(OUTPUT_FOLDER, 'spec_pics') ' !'])
        pause(0.5)
    end;
       
    %% compare to database
    ChooseInitial(target_spec);
    [Whole_init] = Process_Chooese_DB_result(num_init);
    delete 'RmspofF*.txt'
    movefile('DB_res.csv', OUTPUT_FOLDER)

    %% fitting
    result_arr = fitting(target_spec, Whole_init, OUTPUT_FOLDER, target_name);
%     result_arr = fitting(target_spec, Whole_init(1, :), OUTPUT_FOLDER, target_name);
    Process_fitting_result('Whole_spec', result_arr);
    movefile('fit_res.csv', OUTPUT_FOLDER);
    copyfile(target_spec, OUTPUT_FOLDER);
    
end

%% function
function [Whole_init]=Process_Chooese_DB_result(num_init)
global fitThickness
    % compare result name
    xlsFile = 'DB_res.csv';
    
    % make sure file not exist
    if exist(xlsFile)~=0; delete(xlsFile); end
    
    % output compare result
    whole_spec=load('RmspofForwardCompareResult.txt');
%     header={'index' 'RMSP' 'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' };
%     header={'index' 'RMSP' 'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4'  'fwater2' 'fwater3' 'fwater4' 'fcol2' 'flipid3' 'fcol4' };
%     header={'index' 'RMSP' 'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'flipid3' 'fcol4' };
%     header={'index' 'RMSP' 'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'fcol4' };
%       header={'index' 'RMSP' 'th1', 'th2', 'th3' 'f_mel' 'Chb2' 'f_blood2' 'alpha2' 'Chb3' 'f_blood3' 'alpha3' 'Chb4' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'flipid3' 'fcol4' };
    if fitThickness == true
        header={'index' 'RMSP' 'th1' 'th2' 'th3' 'fmel'  'Chb2' 'alpha2' 'Chb3'  'alpha3' 'Chb4' 'alpha4' 'A1'       'k1'   'A2'       'k2'     'A3'    'k3'    'A4'   'k4' 'fcol2' 'flipid3' 'flipid4'};
    else
        header={'index' 'RMSP' 'fmel'  'Chb2' 'alpha2' 'Chb3'  'alpha3' 'Chb4' 'alpha4' 'A1'       'k1'   'A2'       'k2'     'A3'    'k3'    'A4'   'k4' 'fcol2' 'flipid3' 'flipid4'};
    end
        table = array2table(whole_spec, 'VariableNames', header);
    writetable(table, xlsFile);
    Whole_init=whole_spec(1:num_init,3:end);  
end

function Process_fitting_result(sheetName,result_arr)
global tissue_type do_MC_sim fitThickness;
    % fitting result name
    xlsFile = 'fit_res.csv';
    
    % output fitting result
%     header={'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'RMSP'};
%     header={'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fwater2' 'fwater3' 'fwater4' 'fcol2' 'flipid3' 'fcol4' 'RMSP'};
%     header={'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'flipid3' 'fcol4' 'RMSP'};
%     header={'th1', 'th2', 'th3' 'f_mel' 'Chb' 'f_blood2' 'alpha2' 'f_blood3' 'alpha3' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'flipid3' 'RMSP'};
%       header={'th1', 'th2', 'th3' 'f_mel' 'Chb2' 'f_blood2' 'alpha2' 'Chb3' 'f_blood3' 'alpha3' 'Chb4' 'f_blood4' 'alpha4' 'A1' 'k1' 'A2' 'k2' 'A3' 'k3' 'A4' 'k4' 'fcol2' 'flipid3' 'fcol4' 'RMSP'};
    header={'th1'  'th2' 'th3'  'fmel'  'Chb2' 'alpha2' 'Chb3'  'alpha3' 'Chb4' 'alpha4' 'A1'       'k1'   'A2'       'k2'     'A3'    'k3'    'A4'   'k4' 'fcol2' 'flipid3' 'flipid4' 'RMSP'};
    if do_MC_sim==1
        header={header{:} 'MCML-RMSP'};
    end
    table = array2table(result_arr, 'VariableNames', header);
    writetable(table, xlsFile);
end