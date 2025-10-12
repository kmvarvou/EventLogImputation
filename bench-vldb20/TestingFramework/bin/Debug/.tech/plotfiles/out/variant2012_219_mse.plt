set terminal postscript eps enhanced color "Helvetica" 30
set output "error/plots/variant2012_219_mse.eps"

set xrange [90-1:100+1]
set xtics 90,10
set yrange [0:1]
#set log y

set key above width -2 vertical maxrows 3
set tmargin 4.0

set xlabel "percentage of missing values"
set ylabel "mean squared error" offset 1.5 

plot\
	'error/mse/MSE_dynammo.dat' index 0 using 1:2 title 'dynammo' with linespoints lt 8 dt 2 lw 3 pt 4 lc rgbcolor "red" pointsize 1.2, \


set output "error/plots/variant2012_219_rmse.eps"
set ylabel "root mean squared error" offset 1.5 

plot\
	'error/rmse/RMSE_dynammo.dat' index 0 using 1:2 title 'dynammo' with linespoints lt 8 dt 2 lw 3 pt 4 lc rgbcolor "red" pointsize 1.2, \

set output "error/plots/variant2012_219_mae.eps"
set ylabel "mean absolute error" offset 1.5 

plot\
	'error/mae/MAE_dynammo.dat' index 0 using 1:2 title 'dynammo' with linespoints lt 8 dt 2 lw 3 pt 4 lc rgbcolor "red" pointsize 1.2, \
