
%%
m256 = error_mean_;
r256 = error_rms_;
%%
m136 = error_mean_;
r136 = error_rms_;
%%
m135 = error_mean_;
r135 = error_rms_;
%%
figure();
x = [r135(:,1), r136(:,1), r256(:,1)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μa_{epidermis}');

ylabel('error (%)');
saveas(gcf,'μa_epi.png');
close(gcf);

%%
figure();
x = [r135(:,3), r136(:,3), r256(:,3)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μa_{dermis}');

ylabel('error (%)');
saveas(gcf,'μa_dermis.png');
close(gcf);

%%
figure();
x = [r135(:,5), r136(:,5), r256(:,5)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μa_{subcutaneous}');

ylabel('error (%)');
saveas(gcf,'μa_subcutaneous.png');
close(gcf);

%%
figure();
x = [r135(:,7), r136(:,7), r256(:,7)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μa_{muscle}');

ylabel('error (%)');
saveas(gcf,'μa_muscle.png');
close(gcf);

%%
figure();
x = [r135(:,2), r136(:,2), r256(:,2)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μs_{epidermis}');

ylabel('error (%)');
saveas(gcf,'μs_epi.png');
close(gcf);

%%
figure();
x = [r135(:,4), r136(:,4), r256(:,4)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μs_{dermis}');

ylabel('error (%)');
saveas(gcf,'μs_dermis.png');
close(gcf);

%%
figure();
x = [r135(:,6), r136(:,6), r256(:,6)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μs_{subcutaneous}');

ylabel('error (%)');
saveas(gcf,'μs_subcutaneous.png');
close(gcf);

%%
figure();
x = [r135(:,8), r136(:,8), r256(:,8)];
g1 = repmat({'SDS 1 3 5'},40,1);
g2 = repmat({'SDS 1 3 6'},40,1);
g3 = repmat({'SDS 2 4 6'},40,1);
g = [g1; g2; g3];
boxplot(x, g)
title('RMSPE of μs_{muscle}');

ylabel('error (%)');
saveas(gcf,'μs_muscle.png');
close(gcf);