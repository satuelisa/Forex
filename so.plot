set term postscript eps color font ",28"
set size 4, 2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox
set datafile separator ','
set ylabel 'Price'
set xlabel 'Time'
set xdata tim
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d"
set xtics rotate by 90 right
set autoscale xfix
set datafile missing 'NA'
set style fill solid noborder

set key outside right
set xrange ["2020-01-01":"2020-12-31"]
set output 'so.eps'
set arrow from graph 0, 20 to graph 1,20 nohead lt -1 lw 4 
set arrow from graph 0, 80 to graph 1,80 nohead lt -1 lw 4
show arrow
plot 'so.csv' using 1:2 title '14-day' with lines lt -1 lw 8 lc rgb '#009900', \
     '' using 1:3 title 'SMA-3' with lines lt -1 lw 8 lc rgb '#ff0000'
unset arrow

