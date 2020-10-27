from math import fabs
from period import before, after, start, end
from sys import argv

filename = argv[1]
print('''set term postscript eps color
set size 2, 1
set xlabel 'Time'
set xdata time
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d %H:00"
set autoscale xfix''')
print(f'set xrange ["{start:%Y-%m-%d}-01":"{end:%Y-%m-%d}-23"]')
print('''set key outside Right
set pointsize 0.9''')
ds = filename.split('.')[0]
print(f'set output "zz{ds}.eps"')
print(' set ylabel "Closing price"')
threshold = {3: 0.1,
        2: 0.05,
        1: 0.01}
s = {3: 12, 2: 10, 1: 8}
hist = dict()
when = dict()
df = dict()
prev = None
offset = 0.0005
labels = dict()
for kind in threshold:
    hist[kind] = []
    when[kind] = []
    df[kind] =  open(f'zz_{kind}_{filename}', 'w')
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
                                    if after(loc): # in the plotted range
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#ff0000"')
                            if hist[k][0] < hist[k][1] and hist[k][1] > hist[k][2]:
                                if labels.get(loc, (0, 0))[0] < k:
                                    labels[loc] = (k, f'set label "{k}" at "{loc}", {value + offset} font ",{s[k]}" tc rgb "#009900"', 1)
                                    if after(loc): # in the plotted range                                    
                                        print(f'set arrow from "{loc}", graph 0 to "{loc}", graph 1 nohead lt -1 dt 3 lw 1 lc rgb "#00dd00"')
            prev = curr
for k in threshold:
    df[k].close()
with open(f'zzs_{filename}', 'w') as semaphore:
    for loc in labels:
        l = labels[loc]
        if after(loc):
            print(l[1])
        print(f'{loc} {l[0]} {l[-1]}', file = semaphore)
print('''show arrow
show label
plot "demo.dat" using 6:5 title "Closing price" with points lt -1 pt 7 lc rgb "#000000", \\''')
print(f'"zz_1_{filename}" using 1:2 title "Smallest threshold" with line lt -1 lw 3 lc rgb "#999900", \\')
print(f'"zz_2_{filename}" using 1:2 title "Middle threshold" with lines lt -1 lw 5 lc rgb "#009999", \\')
print(f'"zz_3_{filename}" using 1:2 title "Largest threshold" with lines lt -1 lw 7 lc rgb "#990099"')





