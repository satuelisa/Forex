from sys import argv

windows = [3, 5, 7, 9, 11]            

if __name__ == '__main__':
    series = []
    dates = []
    filename = argv[1]
    with open(filename) as data:
        data.readline() # skip header row
        for line in data:
            if 'null' in line:
                continue # skip incomplete data
            fields = line.split(',') # CSV
            if len(fields) > 0:
                dates.append(fields[0])
                series.append(float(fields[4])) # closing price

    for l in windows:
        # rolling average
        window = [series[0]]
        t = 0
        with open(f'sma_{l}.csv', 'w') as target:
            for value in series[1:]:
                window.append(value)
                print(f'{dates[t]},{sum(window) / len(window)}', file = target)
                if 'stdout' in argv:
                    print(f'sma,{l},{dates[t]},{sum(window) / len(window)}')                    
                if len(window) == l:
                    window.pop(0)
                t += 1
        # EMA
        rho = 2 / (l + 1)
        curr = series[0]
        t = 0
        with open(f'ema_{l}.csv', 'w') as target:
            for value in series[1:]:
                assert value > 0
                print(f'{dates[t]},{curr}', file = target)
                if 'stdout' in argv:
                    print(f'ema,{l},{dates[t]},{curr}')                    
                curr = rho * value + (1 - rho) * curr
                t += 1
        with open('avg.plot', 'w') as target:
            print(f'''set term postscript eps color font ",28"
set size 3.5, 2.2
set palette defined (-1 '#ff0000', 1 '#009900')
set cbrange [-1:1]
unset colorbox
set datafile separator ','
set ylabel 'Price'
set xlabel 'Time'
set xdata tim
set timefmt "%Y-%m-%d-%H"
set format x "%Y-%m-%d"
set xtics rotate by 90 right
set autoscale xfix
set xrange ["2020-05-01":"2020-07-31"]
set datafile missing 'NA'
set style fill solid noborder
set boxwidth 20000 absolute # 4 hrs 1800 approx
set output 'sma.eps'
plot '{filename}' using 1:2:4:3:5:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3,'sma_3.csv' using 1:2 with lines lt 1 dt 1 lw 8 title 'SMA 3','sma_7.csv' using 1:2 with lines lt 2 dt 2 lw 8 title 'SMA 7','sma_11.csv' using 1:2 with lines lt 3 dt 3 lw 8 title 'SMA 11'
set output 'ema.eps'
plot '{filename}' using 1:2:4:3:4:($5 < $2 ? -1 : 1) notitle with candlesticks palette lw 3,'ema_3.csv' using 1:2 with lines lt 1 dt 1 lw 8 title 'EMA 3','ema_7.csv' using 1:2 with lines lt 2 dt 2 lw 8 title 'EMA 7','ema_11.csv' using 1:2 with lines lt 3 dt 3 lw 8 title 'EMA 11'
''', file = target)
