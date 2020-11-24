from period import postpone
from math import fabs
from avg import windows

horizons = [1, 2, 3, 4, 7, 14, 21] # forecast horizon in days
thresholds = [x for x in range(1, 10, 2)] # % change in closing price

if __name__ == "__main__":
    raw = dict()
    with open('daily.dat') as data:
        for line in data:
            fields = line.split()
            date = '-'.join(fields[-1].split('-')[:-1]) # remove the hour                
            closing = fields[3]
            raw[date] = closing
    sma = dict()
    for window in windows:
        sma[window] = dict()
        with open(f'sma_{window}.dat') as data:
            for line in data:
                fields = line.split()
                date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
                avg = fields[1]
                sma[window][date] = 1 * (avg < raw[date])
    ema = dict()
    for window in windows:
        ema[window] = dict()
        with open(f'ema_{window}.dat') as data:
            for line in data:
                fields = line.split()
                date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
                avg = fields[1]
                ema[window][date] = 1 * (avg < raw[date])
    ha = dict()
    with open('ha.dat') as data:
        for line in data:
            fields = line.split()
            date = '-'.join(fields[-1].split('-')[:-1]) # remove the hour        
            hao = fields[0]
            hac = fields[3]
            ha[date] = 1 * (hao < hac)
    zzs = dict()
    with open('zzs.dat') as data:
        for line in data:
            fields = line.split()
            date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
            level = fields[1]
            kind = fields[2]
            zzs[date] = level + ' ' + kind
    so = dict()
    with open('so.dat') as data:
        for line in data:        
            fields = line.split()
            date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
            so[date] = 1 * (float(fields[-1]) > float(fields[-2])) # binary (above or below)
    rsi = dict()
    with open('rsi.dat') as data:
        for line in data:        
            fields = line.split()
            date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
            value = float(fields[-1])
            rsi[date] = int(value) // 20 # [0, 100] discretized to five levels [0, 4]
    ms = dict()                                                      
    with open ('macd_sma.dat') as data:
        for line in data:                
            if 'macd' in line:
                fields = line.split()
                date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
                value = float(fields[-2])
                ms[date] = 1 * (value > 0) # binary (positive or negative)
    me = dict()                                                      
    with open ('macd_ema.dat') as data:
        for line in data:                
            if 'macd' in line:
                fields = line.split()
                date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
                value = float(fields[-2])
                me[date] = 1 * (value > 0) # binary (positive or negative)
    complete = set(raw.keys()) & set(ha.keys()) & set(zzs.keys()) & set(so.keys()) & set(rsi.keys()) & set(ms.keys()) & set(me.keys())
    for w in windows:
        complete = complete & set(sma[w].keys())
        complete = complete & set(ema[w].keys())
    indicators = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['H-A ZZS-level ZZS-kind SO RSI MACD-SMA MACD-EMA']
    for td in horizons:
        for thr in thresholds:
            with open(f'char_{td}_{thr}.dat', 'w') as output:
                classes =  [f'HT-{td}-{thr}-above HT-{td}-{thr}-sign']
                print('Date ' + ' '.join(indicators + classes), file = output)
                semaphore = None
                for date in sorted(list(complete)):
                    baseline = float(raw[date])
                    forecasts = ''
                    skip = False
                    semaphore = zzs[date] if date in zzs else semaphore
                    if semaphore is not None:
                        later = raw.get(postpone(date, td), None)
                        if later is not None: # data for that day not available
                            perc = 100 * ((float(later) - baseline) / baseline) 
                            forecasts = f'{1 * (fabs(perc) >= thr)} {1 * (perc > 0)}'
                            print(date, ' '.join([str(sma[w][date]) for w in windows]), \
                                  ' '.join([str(ema[w][date]) for w in windows]), \
                                  ha[date], semaphore, so[date], rsi[date], ms[date], me[date], forecasts, file = output)
