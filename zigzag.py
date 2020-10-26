from math import fabs
from period import before, after, start, end

print('''set term postscript eps color
set size 2, 1
set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d %H:00"
set autoscale xfix''')
print(f'set xrange ["{start:%Y-%m-%d}-01":"{end:%Y-%m-%d}-23"]')
print('''set key outside Right
set pointsize 0.9
set output "zz.eps"
set ylabel "Closing price"''')
threshold = {3: 0.1,
        2: 0.05,
        1: 0.01}
s = {3: 12, 2: 10, 1: 8}
hist = dict()
when = dict()
df = dict()
prev = None
offset = 0.0005
for kind in threshold:
    hist[kind] = []
    when[kind] = []
    df[kind] =  open(f'zz_{kind}.dat', 'w')
labels = dict()
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        if len(data) > 0:
            step = int(data[0])
            date = data[-1]
            curr = float(data[4]) # closing
            if prev is not None:
                d = 100 * fabs(curr - prev) / prev
                for k in [3, 2, 1]:
                    if d > threshold[k]:
                        print(date, curr, file = df[k])
                        while len(hist[k]) > 2:
                            hist[k].pop(0)
                            when[k].pop(0)
                        hist[k].append(curr)
                        when[k].append(date)
                        if len(hist[k]) == 3:
                            loc = when[k][1]
                            if after(loc): # in the plotted range
                                value = hist[k][1]
                                if hist[k][0] > hist[k][1] and hist[k][1] < hist[k][2]:
                                    if labels.get(loc, (0, 0))[0] < k:
                                        labels[loc] = (k, f'set label "{k}" at "{loc}", {value - offset} font ",{s[k]}" tc rgb "#dd0000"')
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#ff0000"')
                                if hist[k][0] < hist[k][1] and hist[k][1] > hist[k][2]:
                                    if labels.get(loc, (0, 0))[0] < k:
                                        labels[loc] = (k, f'set label "{k}" at "{loc}", {value + offset} font ",{s[k]}" tc rgb "#009900"')
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#00dd00"')
            prev = curr
for k in threshold:
    df[k].close()
for l in labels.values():
    print(l[1])
print('''show arrow
show label
plot "demo.dat" using 6:5 title "Closing price" with points lt -1 pt 7 lc rgb "#000000", \
     "zz_1.dat" using 1:2 title "Smallest threshold" with line lt -1 lw 3 lc rgb "#999900", \
     "zz_2.dat" using 1:2 title "Middle threshold" with lines lt -1 lw 5 lc rgb "#009999", \
     "zz_3.dat" using 1:2 title "Largest threshold" with lines lt -1 lw 7 lc rgb "#990099"''')





