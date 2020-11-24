set term postscript eps color font ",28"
set size 3, 2.2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox

set ylabel 'Price'
set xlabel 'Time'
set xdata tim
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d %H:00"
set xtics rotate by 90 right
set autoscale xfix
set datafile missing 'NA'
set style fill solid noborder
set yrange [1.24:1.35]
set ytics 1.2, 0.01
set output 'demo.eps'
set xrange ["2010-07-15-23":"2010-08-30-23"]
set key at "2010-08-25-00", graph 0.8

set boxwidth 20000 absolute # 4 hrs 1800 approx

plot 'daily.dat' using 5:1:2:3:4:($4 < $1 ? -1 : 1) notitle with candlesticks palette lw 3

set output 'ha.eps'
plot 'ha.dat' using 5:1:2:3:4:($4 < $1 ? -1 : 1) notitle with candlesticks palette lw 3

set output 'sma.eps'
plot 'daily.dat' using 5:1:2:3:4:($4 < $1 ? -1 : 1) notitle with candlesticks palette lw 3, \
     'sma_3.dat' using 1:2 with lines lt 1 dt 1 lw 8 title 'SMA 5', \
     'sma_7.dat' using 1:2 with lines lt 2 dt 2 lw 8 title 'SMA 21', \
     'sma_21.dat' using 1:2 with lines lt 3 dt 3 lw 8 title 'SMA 89'

set output 'ema.eps'
plot 'daily.dat' using 5:1:2:3:4:($4 < $1 ? -1 : 1) notitle with candlesticks palette lw 3, \
     'ema_3.dat' using 1:2 with lines lt 1 dt 1 lw 8 title 'EMA 5', \
     'ema_7.dat' using 1:2 with lines lt 2 dt 2 lw 8 title 'EMA 21', \
     'ema_21.dat' using 1:2 with lines lt 3 dt 3 lw 8 title 'EMA 89'

set yrange [-0.022:0.025]
set ytics -0.02, 0.01
set ylabel 'Difference'
set pointsize 1.5
set key at 30, graph 0.9

set output 'macd_sma.eps'
plot 'macd.dat' using 1:(stringcolumn(3) eq "sma_diff" ? column(2) : 1/0) title 'Difference' with boxes lc rgb '#000000', \
     '' using 1:(stringcolumn(3) eq "sma_macd" ? column(2) : 1/0) title 'MACD with EMA' with points pt 7 lc rgb '#ff0000'

set output 'macd_ema.eps'
plot 'macd.dat' using 1:(stringcolumn(3) eq "ema_diff" ? column(2) : 1/0) title 'Difference' with boxes lc rgb '#000000', \
     '' using 1:(stringcolumn(3) eq "ema_macd" ? column(2) : 1/0) title 'MACD with EMA' with points pt 7 lc rgb '#ff0000'

set yrange[-5:115]
set ytics 0, 20
set ylabel 'Stochactic oscillator'
set pointsize 1.5
unset key

set output 'so.eps'
set arrow from graph 0, 20 to graph 1,20 nohead lt -1 lw 4 
set arrow from graph 0, 80 to graph 1,80 nohead lt -1 lw 4
show arrow
plot 'so.dat' using 1:2 title '14-day window' with lines lt -1 lw 8 lc rgb '#009900', \
     '' using 1:3 title 'SMA 3' with lines lt -1 lw 8 lc rgb '#ff0000'
unset arrow

set output 'rsi.eps'
set ylabel 'RSI'
set arrow from graph 0,30 to graph 1,30 nohead lt -1 lw 8 dt 2 lc rgb '#009900'
set arrow from graph 0,50 to graph 1,50 nohead lt -1 lw 6
set arrow from graph 0,70 to graph 1,70 nohead lt -1 lw 8 dt 2 lc rgb '#ff0000'
show arrow
plot 'rsi.dat' using 1:2 title 'RSI' with lines lt -1 lw 8 lc rgb '#0000ff'
unset arrow


