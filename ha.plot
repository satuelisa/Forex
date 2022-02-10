set term postscript eps color font ",28"
set size 7, 2.2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox

set ylabel 'Price'
set xlabel 'Time'
set xdata tim
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d"
set xrange ["2020-01-01":"2020-12-31"]
set xtics rotate by 90 right
set autoscale xfix
set datafile separator ','
set datafile missing 'NA'
set style fill solid noborder
set boxwidth 20000 absolute # 4 hrs 1800 approx

set output 'ha.eps'
plot 'ha.csv' using 5:1:2:3:4:($4 < $1 ? -1 : 1) notitle with candlesticks palette lw 3
