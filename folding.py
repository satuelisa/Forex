from period import before, after, dt, getStart, getEnd, setStart, setEnd
from sys import argv

past = []
minima = []
maxima = []
up = None
down = None

setStart(2016, 9, 7)
setEnd(2021, 9, 7)

plot = open('fold.plot', 'w')
print('''set term postscript eps color font ",28"
set size 3, 2.2

set xlabel 'Time'
set xdata time

set palette defined (1 '#ff0000', 2 '#009900', 3 '#990000', 4 '#007700', 5 '#000000')
set cbrange [1:5]
unset colorbox

set style fill solid noborder
set datafile separator ','
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set xtics rotate by 90 right
set autoscale xfix
set datafile missing 'NA'
set style fill solid noborder''', file = plot)
print(f'#set xrange ["{getStart():%Y-%m-%d}-01":"{getEnd():%Y-%m-%d}-23"]', file = plot)
print('''#set yrange [1.048:1.065]
#set ytics 1.05, 0.01
unset key
set pointsize 1.2''', file = plot)
ext = open('extrema.csv', 'w')
last = None
with open(argv[1]) as data:
    data.readline() # skip header
    for line in data:
        if 'null' in line:
            continue # skip incomplete
        data = line.split(',') # CSV
        if len(data) == 0:
            continue
        t = data[0]
        if not after(t): # process only the intended period
            continue
        if not before(t):
            continue
        y = float(data[4]) # closing price 
        past.append((y,  t))
        if len(past) > 2:
            y1, t1 = past[-2]
            if past[-3][0] > y1 and y1 < y: # the second to last data point was a local minimum
                print(f'{t1},{y1},1', file = ext)
                minima.append((y1, t1))                                                            
                if down is None and len(minima) > 1:
                    prev = minima[-2] # the immediate previous local minima
                    y0 = prev[0]
                    t0 = prev[1] 
                    a = (y1 - y0) / dt(t1, t0) # slope between the two
                    if a > 0 and (up is None or a > up[2]):
                        if after(t1) and before(t1): 
                            print(f'set arrow from "{t1}", graph 0 to "{t1}", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#ff0000"', file = plot)
                        up = t0, y0, a
                continue                        
            if past[-3][0] < y1 and y1 > y: # the second to last data point was a local maximum
                print(f'{t1},{y1},2', file = ext)
                maxima.append((y1, t1))                                                            
                if up is None and len(maxima) > 1:
                    prev = maxima[-2] # the immediate previous local minima
                    y0 = prev[0]
                    t0 = prev[1]
                    a = (y1 - y0) / dt(t1, t0) # slope between the two
                    if a < 0 and (down is None or a < down[2]):
                        if after(t1) and before(t1):                         
                            print(f'set arrow from "{t1}", graph 0 to "{t1}", graph 1 nohead lt -1 dt 3 lw 2 lc rgb "#00dd00"', file = plot)
                        down = t0, y0, a
                continue
            assert not (up and down)
            if up is not None:
                t0, y0, a = up
                projection = y0 + a * dt(t1, t0)
                if projection >= y1:
                    if last is None or t0 > last:
                        if after(t0):
                            print(f'set arrow from "{t0}", {y0} to "{t1}", {projection} nohead lt -1 lw 6 lc rgb "#ff0000"', file = plot)
                            print(f'{t1},{projection},3', file = ext)
                            print(f'{t1},{y1},5', file = ext)
                        if after(t1) and before(t1):                                                 
                            print(f'set arrow from "{t1}", graph 0 to "{t1}", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#00dd00"', file = plot)
                    up = None
                    last = t1
            if down is not None:
                t0, y0, a = down
                projection = y0 + a * dt(t1, t0)
                if projection <= y1:
                    if last is None or t0 > last:
                        if after(t0):
                            print(f'set arrow from "{t0}", {y0} to "{t1}", {projection} nohead lt -1 lw 6 lc rgb "#00dd00"', file = plot)
                            print(f'{t1},{projection},4', file = ext)
                            print(f'{t1},{y1},5', file = ext)
                        if after(t1) and before(t1):                         
                            print(f'set arrow from "{t1}", graph 0 to "{t1}", graph 1 nohead lt -1 dt 2 lw 2 lc rgb "#ff0000"', file = plot)
                    down = None
                    last = t1
                
ext.close()        
print(f'''show arrow
set output 'fold.eps'
set ylabel 'Closing price'
plot '{argv[1]}' using 1:4 with lines lt -1 lw 3 lc rgb '#0000ff', \
     'extrema.csv' using 1:2:3 with points pt 7 palette''', file = plot)
plot.close()
