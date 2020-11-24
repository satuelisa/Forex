series = []
dates = []
with open('daily.dat') as data:
    for line in data:
        f = line.split()
        if len(f) == 0:
            continue
        dates.append(f[-1])
        series.append(float(f[-2])) # closing price

fast = 12
slow = 26
diff = 9

data = dict()
for l in [fast, slow]:
    data[l] = list()
    rho = 2 / (l + 1)
    t = 0
    curr = series[0]
    window = [curr]
    for value in series[1:]:
        values = dict()
        window.append(value)
        curr = rho * value + (1 - rho) * curr        
        values['sma'] = sum(window) / len(window)
        values['ema'] = curr
        if len(window) == l:
            window.pop(0)
        data[l].append(values)
        t += 1
window = {'sma': [], 'ema': []}
target = {'sma': open('macd_sma.dat', 'w'),
          'ema': open('macd_ema.dat', 'w')}
for step in range(t):
    for kind in ['sma', 'ema']:
        f = data[fast][step][kind]
        s = data[slow][step][kind]
        d = f - s
        window[kind].append(d)
        print(dates[step], d, 'diff', file = target[kind])
        print(dates[step], sum(window[kind]) / len(window[kind]), 'macd', file = target[kind])
        if len(window[kind]) == diff:
            window[kind].pop(0)
        
for t in target.values():
    t.close()
