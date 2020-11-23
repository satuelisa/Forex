from math import fabs
from period import before, after, setStart, setEnd, getStart, getEnd
from sys import argv

threshold = {3: 0.1,
             2: 0.05,
             1: 0.01}

# period to visualize
setStart(2019, 1, 15)
setEnd(2019, 2, 15)

filename = argv[1]
print('''set term postscript eps color font ",18"
set size 2, 1.5
set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d %H:00"
set yrange [1.122:1.152]
set ytics 1.125, 0.005
set xtics rotate by 90 right
set autoscale xfix''')
print(f'set xrange ["{getStart():%Y-%m-%d}-01":"{getEnd():%Y-%m-%d}-23"]')
print('''set key outside Right
set pointsize 0.9''')
ds = filename.split('.')[0]
print(' set ylabel "Closing price"')
print(f'set output "zz{ds}.eps"')
s = {3: 24, 2: 20, 1: 16}
hist = dict()
when = dict()
df = dict()
prev = None
offset = 0.001
labels = dict()
for kind in threshold:
    hist[kind] = []
    when[kind] = []
    df[kind] =  open(f'zz_{kind}.dat', 'w')
with open(filename) as data:
    for line in data:
        if '#' in line:
            continue
        data = line.split()
        if len(data) > 0:
            date = data[-1]
            curr = float(data[3]) # closing
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
                            value = hist[k][1]
                            if hist[k][0] > hist[k][1] and hist[k][1] < hist[k][2]:
                                if labels.get(loc, (0, 0))[0] < k:
                                    labels[loc] = (k, f'set label "{k}" at "{loc}", {value - offset} font ",{s[k]}" tc rgb "#dd0000"', 0)
                                    if after(loc) and before(loc): # in the plotted range
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#ff0000"')
                            if hist[k][0] < hist[k][1] and hist[k][1] > hist[k][2]:
                                if labels.get(loc, (0, 0))[0] < k:
                                    labels[loc] = (k, f'set label "{k}" at "{loc}", {value + offset} font ",{s[k]}" tc rgb "#009900"', 1)
                                    if after(loc) and before(loc): # in the plotted range                                    
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#00dd00"')
            prev = curr
for k in threshold:
    df[k].close()
with open(f'zzs.dat', 'w') as semaphore:
    for loc in labels:
        l = labels[loc]
        if after(loc):
            print(l[1])
        print(f'{loc} {l[0]} {l[-1]}', file = semaphore)
print('show arrow\nshow label')
print('plot "daily.dat" using 5:4 title "Closing price" with points lt -1 pt 7 lc rgb "#000000", \\')
print('"zz_1.dat" using 1:2 title "Smallest threshold" with line lt -1 lw 3 lc rgb "#999900", \\')
print('"zz_2.dat" using 1:2 title "Middle threshold" with lines lt -1 lw 5 lc rgb "#009999", \\')
print('"zz_3.dat" using 1:2 title "Largest threshold" with lines lt -1 lw 7 lc rgb "#990099"')
