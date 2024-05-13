%% This can plot epsilon
%  2022/6/18 by LEE, HAO-WEI
clear; clc; close all;

wl = 700:1:900;
fid_mel = load('epsilon/mel_mua.txt');
fid_hemo = load('epsilon/epsilon.txt');
fid_water = load('epsilon/water_mua.txt');
fid_collagen = load('epsilon/collagen_mua_data.txt');


mu_mel = interp1(fid_mel(:, 1), fid_mel(:, 2), wl, 'spline');
epsilon_oxy = interp1(fid_hemo(:, 1), fid_hemo(:, 2), wl, 'spline');
epsilon_deoxy = interp1(fid_hemo(:, 1), fid_hemo(:, 3), wl, 'spline');
mu_water = interp1(fid_water(:, 1), fid_water(:, 2), wl, 'spline');
mu_collagen = interp1(fid_collagen(:, 1), fid_collagen(:, 2), wl, 'spline');
mu_protein = interp1(fid_collagen(:, 1), fid_collagen(:, 2), wl, 'spline');

%% plot
figure();
grid on;
% plot(wl, log10(mu_mel), ...
%     wl, log10(epsilon_oxy), ...
%     wl, log10(epsilon_deoxy), ...
%     wl, log10(mu_water), ...
%     wl, log10(mu_collagen), ...
%     wl, log10(mu_protein));
plot(wl, mu_mel, ...
    wl, epsilon_oxy, ...
    wl, epsilon_deoxy, ...
    wl, mu_water, ...
    wl, mu_collagen, ...
    wl, mu_protein);
xlabel('Wavelength');
ylabel('Absorption coefficient');
title('Absoprtion 700-900');
legend('mel', 'HbO2', 'Hb', 'water', 'collagen', 'protein');


