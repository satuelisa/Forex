set term postscript eps color font ",28"
set size 3, 1.2

set xlabel 'Time'
set xdata time

set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d %H:00"
set autoscale xfix
set datafile missing 'NA'
set style fill solid noborder
set yrange [1.24:1.31]
set ytics 1.25, 0.01
set xrange ["2010-07-01-01":"2010-07-31-23"]

set style fill solid noborder

unset key


set output 'zz_1.eps'
set ylabel 'Closing price'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_0.1.dat' using 3:2 title 'One percent' with linespoints lt -1 lw 10 lc rgb '#ff0000', \

set output 'zz_2.eps'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_0.2.dat' using 3:2 title 'Half percent' with linespoints lt -1 lw 10 lc rgb '#009900', \

set output 'zz_3.eps'
plot 'demo.dat' using 6:5 title 'Closing' with lines lt -1 lw 6 lc rgb '#000000', \
     'zigzag_0.3.dat' using 3:2 title 'Tenth of a percent' with linespoints lt -1 lw 10 lc rgb '#0000ff'	


