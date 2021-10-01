set term postscript eps color font ",28"
set size 4.5, 2.2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox

set ylabel 'Price'
set xlabel 'Time'
set xdata tim
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d"
set xtics rotate by 90 right
set autoscale xfix
set datafile missing 'NA'
set style fill solid noborder
set datafile separator ','
set output 'rsi.eps'
set ylabel 'RSI'
set key off
set arrow from graph 0,30 to graph 1,30 nohead lt -1 lw 8 dt 2 lc rgb '#009900'
set arrow from graph 0,50 to graph 1,50 nohead lt -1 lw 6
set arrow from graph 0,70 to graph 1,70 nohead lt -1 lw 8 dt 2 lc rgb '#ff0000'
show arrow
plot 'rsi.csv' using 1:2 title 'RSI' with lines lt -1 lw 8 lc rgb '#0000ff'
unset arrow


