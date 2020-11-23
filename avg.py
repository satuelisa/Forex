windows = [3, 5, 7, 14, 21]            

if __name__ == '__main__':
    series = []
    dates = []
    with open('daily.dat') as data:
        for line in data:
            fields = line.split()
            if len(fields) > 0:
                dates.append(fields[-1])
                series.append(float(fields[-2])) # closing price

    for l in windows:
        # rolling average
        window = [series[0]]
        t = 0
        with open(f'sma_{l}.dat', 'w') as target:
            for value in series[1:]:
                window.append(value)
                print(dates[t], sum(window) / len(window), file = target)
                if len(window) == l:
                    window.pop(0)
                t += 1
        # EMA
        rho = 2 / (l + 1)
        curr = series[0]
        t = 0
        with open(f'ema_{l}.dat', 'w') as target:
            for value in series[1:]:
                assert value > 0
                print(dates[t], curr, file = target)
                curr = rho * value + (1 - rho) * curr
                t += 1

