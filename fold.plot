set term postscript eps color font ",28"
set size 3, 1.2

set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set autoscale xfix

set palette defined (1 '#ff0000', 2 '#009900', 3 '#990000', 4 '#007700', 5 '#000000')
set cbrange [1:5]
unset colorbox

set style fill solid noborder
set xrange ["2019-12-31":"2020-10-01"]
set yrange [1.04:1.21]
set ytics 1.05, 0.05
unset key
set pointsize 1.2
set arrow from "2020-01-13", graph 0 to "2020-01-13", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-01-06", 1.1195 to "2020-01-16", 1.1109285714285713 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-01-16", graph 0 to "2020-01-16", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-01-20", graph 0 to "2020-01-20", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-01-28", graph 0 to "2020-01-28", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-01-22", 1.1093 to "2020-01-30", 1.0998333333333334 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-01-30", graph 0 to "2020-01-30", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-02-11", graph 0 to "2020-02-11", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-01-31", 1.1094 to "2020-02-21", 1.0754181818181816 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-02-21", graph 0 to "2020-02-21", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-03-04", graph 0 to "2020-03-04", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-03-16", graph 0 to "2020-03-16", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-03-27", graph 0 to "2020-03-27", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-04-07", graph 0 to "2020-04-07", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-03-27", 1.1142 to "2020-04-09", 1.0845363636363636 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-04-09", graph 0 to "2020-04-09", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-04-13", graph 0 to "2020-04-13", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-04-17", graph 0 to "2020-04-17", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-04-27", graph 0 to "2020-04-27", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-05-08", graph 0 to "2020-05-08", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-05-01", 1.0985 to "2020-05-13", 1.0738142857142858 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-05-13", graph 0 to "2020-05-13", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-05-25", graph 0 to "2020-05-25", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-06-05", graph 0 to "2020-06-05", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-05-25", 1.09 to "2020-06-08", 1.1391272727272728 nohead lt -1 lw 6 lc rgb "#ff0000"
set arrow from "2020-06-08", graph 0 to "2020-06-08", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#00dd00"
set arrow from "2020-06-15", graph 0 to "2020-06-15", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-06-10", 1.1371 to "2020-06-22", 1.1258200000000003 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-06-22", graph 0 to "2020-06-22", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-06-23", graph 0 to "2020-06-23", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-06-29", graph 0 to "2020-06-29", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-06-23", 1.1308 to "2020-07-03", 1.1198000000000001 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-07-03", graph 0 to "2020-07-03", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
set arrow from "2020-07-07", graph 0 to "2020-07-07", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-07-16", graph 0 to "2020-07-16", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-07-28", graph 0 to "2020-07-28", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-07-16", 1.1384 to "2020-07-31", 1.1799 nohead lt -1 lw 6 lc rgb "#ff0000"
set arrow from "2020-07-31", graph 0 to "2020-07-31", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#00dd00"
set arrow from "2020-08-03", graph 0 to "2020-08-03", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-08-19", graph 0 to "2020-08-19", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-08-10", 1.1736 to "2020-08-21", 1.185822222222222 nohead lt -1 lw 6 lc rgb "#ff0000"
set arrow from "2020-08-21", graph 0 to "2020-08-21", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#00dd00"
set arrow from "2020-08-25", graph 0 to "2020-08-25", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-08-27", graph 0 to "2020-08-27", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"
set arrow from "2020-09-14", graph 0 to "2020-09-14", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-09-17", graph 0 to "2020-09-17", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-09-24", graph 0 to "2020-09-24", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"
set arrow from "2020-09-17", 1.1847 to "2020-09-28", 1.1572 nohead lt -1 lw 6 lc rgb "#00dd00"
set arrow from "2020-09-28", graph 0 to "2020-09-28", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"
show arrow
set output 'fold.eps'
set ylabel 'Closing price'
plot 'demo.dat' using 6:5 with lines lt -1 lw 5 lc rgb '#0000ff',      'extrema.dat' using 1:2:3 with points pt 7 palette
