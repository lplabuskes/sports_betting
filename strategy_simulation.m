bet_portions = [.0309 .0649 .0129 .012 .0004 .0013 .0128 .0038];
odds = [2.05 1.667 2.1 3 1.787 1.758 1.758 2.35];
win_percent = [.52 .65 .49 .35 .56 .57 .58 .43];

win_return = bet_portions.*(odds-1);
lose_return = -bet_portions;

n_bets = length(bet_portions);
n_days = 100;
n_sims = 10000;

samples = rand(n_bets, n_days, n_sims);
samples = samples<win_percent';
percent_change = zeros(n_sims,n_days);
for i = 1:n_sims
    percent_change(i,:) = win_return*samples(:,:,i) + lose_return*not(samples(:,:,i));
end
total = cumprod(1+percent_change,2);
subplot(131)
plot(median(total))
title('Median')
axis square
subplot(132)
plot(min(total))
title('Minimum')
axis square
subplot(133)
plot(max(total))
title('Maximum')
axis square
