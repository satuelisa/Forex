set term postscript eps color font ",28"
set size 4, 2.2
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

set xrange ["2020-01-01":"2020-12-31"]

set boxwidth 20000 absolute # 4 hrs 1800 approx

set ylabel 'Difference'
set pointsize 1.5
set key at 30, graph 0.9

set output 'macd_sma.eps'
plot 'macd_sma.csv' using 1:(stringcolumn(3) eq "diff" ? column(2) : 1/0) title 'Difference' with boxes lc rgb '#000000', \
     '' using 1:(stringcolumn(3) eq "macd" ? column(2) : 1/0) title 'MACD with EMA' with points pt 7 lc rgb '#ff0000'

set output 'macd_ema.eps'
plot 'macd_ema.csv' using 1:(stringcolumn(3) eq "diff" ? column(2) : 1/0) title 'Difference' with boxes lc rgb '#000000', \
     '' using 1:(stringcolumn(3) eq "macd" ? column(2) : 1/0) title 'MACD with EMA' with points pt 7 lc rgb '#ff0000'

