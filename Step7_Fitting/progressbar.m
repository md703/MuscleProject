
function progressbar(i, percent)
    % note multiple spaces at the end - that's a scratchpad area
    len = 46;
    if i == 1
        fprintf('    Counter_lsqcurfit = %5d, RMSP = %10.4f%% ', i, percent); % 43 char 22
    else
        % backspace 6 positions before printing %5.2f%% (uses 6 positions)
        back_str = repmat('\b', 1, len);
        fprintf(back_str);
        fprintf('Counter_lsqcurfit = %5d, RMSP = %10.4f%% ', i, percent);
    end
end

