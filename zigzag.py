from math import fabs

thr = [0.01, 0.05, 0.1]
target = dict()
for t in thr:
    target[t] = open(f'zigzag_{t}.dat', 'w')
prev = None
last = None
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        if len(data) > 0:
            step = int(data[0])
            date = data[-1]
            curr = float(data[4]) # closing
            if prev is not None:
                d = 100 * fabs(curr - prev) / prev
                for t in thr:
                    if d > t:
                        print(step, curr, date, file = target[t])
            prev = curr
for t in thr:
    target[t].close()


