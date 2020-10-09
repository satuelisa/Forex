set term postscript eps color font ",28"
set size 3, 1.2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox

set key at 25, graph 0.9
set ylabel 'Price'
set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
#set xtics rotate by 90 right
set autoscale xfix

set style fill solid noborder
set yrange [1.06:1.16]
set ytics 1.075, 0.025

set output 'demo.eps'
set xrange ["2019-12-31":"2020-05-31"]

set boxwidth 37500 absolute

plot 'demo.dat' using 6:2:3:4:5:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3

set output 'ha.eps'
plot 'ha.dat' using 6:2:3:4:5:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3

set output 'sma.eps'
plot 'demo.dat' using 6:2:3:4:5:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3, \
     'roll_5.dat' using 1:2 with lines lt 1 dt 1 lw 8 title 'SMA 5', \
     'roll_21.dat' using 1:2 with lines lt 2 dt 2 lw 8 title 'SMA 21', \
     'roll_89.dat' using 1:2 with lines lt 3 dt 3 lw 8 title 'SMA 89'

set output 'ema.eps'
plot 'demo.dat' using 6:2:3:4:5:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3, \
     'ema_5.dat' using 1:2 with lines lt 1 dt 1 lw 8 title 'EMA 5', \
     'ema_21.dat' using 1:2 with lines lt 2 dt 2 lw 8 title 'EMA 21', \
     'ema_89.dat' using 1:2 with lines lt 3 dt 3 lw 8 title 'EMA 89'

set yrange [-0.019:0.021]
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

set xrange ["2019-12-31":"2020-10-01"]
set yrange[-5:105]
set ytics 0, 20
set ylabel 'Stochactic oscillator'
set pointsize 1.5
unset key

set output 'so.eps'
set arrow from "2020-01-01",20 to "2020-09-30",20 nohead lt -1 lw 4 
set arrow from "2020-01-01",80 to "2020-09-30",80 nohead lt -1 lw 4
show arrow
plot 'so.dat' using 1:2 title '14-day window' with lines lt -1 lw 8 lc rgb '#009900', \
     '' using 1:3 title 'SMA 3' with lines lt -1 lw 8 lc rgb '#ff0000'
unset arrow

set output 'rsi.eps'
set ylabel 'RSI'
set arrow from "2020-01-01",30 to "2020-09-30",30 nohead lt -1 lw 8 dt 2 lc rgb '#009900'
set arrow from "2020-01-01",50 to "2020-09-30",50 nohead lt -1 lw 6
set arrow from "2020-01-01",70 to "2020-09-30",70 nohead lt -1 lw 8 dt 2 lc rgb '#ff0000'
show arrow
plot 'rsi.dat' using 1:2 title 'RSI' with lines lt -1 lw 8 lc rgb '#0000ff'
unset arrow


