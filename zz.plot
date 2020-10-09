set term postscript eps color font ",28"
set size 3, 1.2

set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set autoscale xfix

set style fill solid noborder
set xrange ["2019-12-31":"2020-10-01"]
unset key
set yrange [1.04:1.21]
set ytics 1.05, 0.05

set output 'zz_1.eps'
set ylabel 'Closing price'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_1.0.dat' using 3:2 title 'One percent' with linespoints lt -1 lw 10 lc rgb '#ff0000', \

set output 'zz_2.eps'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_0.5.dat' using 3:2 title 'Half percent' with linespoints lt -1 lw 10 lc rgb '#009900', \

set output 'zz_3.eps'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_0.1.dat' using 3:2 title 'Tenth of a percent' with linespoints lt -1 lw 10 lc rgb '#0000ff'	


