from avg import windows
from math import fabs
from time import time
from sys import argv
import datetime
from period import fmt, final

horizons = [1, 2, 3, 4, 5, 10, 15] # forecast horizon in trading days
thresholds = [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0] # % change in closing price

if __name__ == "__main__":
    print('Characterization begins')
    start = time()
    raw = dict()
    filename = argv[1]
    with open(filename) as data:
        data.readline() # skip header
        for line in data:
            if 'null' not in line: # only complete lines
                line = line.strip()
                fields = line.split(',') # CSV
                date = fields[0]
                closing = fields[4]
                raw[date] = closing
    sma = dict()
    for window in windows:
        sma[window] = dict()
        with open(f'sma_{window}.csv') as data:
            for line in data:
                line = line.strip()                
                fields = line.split(',')
                date = fields[0]
                avg = fields[1]
                sma[window][date] = 1 * (avg < raw[date])
    ema = dict()
    for window in windows:
        ema[window] = dict()
        with open(f'ema_{window}.csv') as data:
            for line in data:
                line = line.strip()                
                fields = line.split(',')
                date = fields[0]        
                avg = fields[1]
                ema[window][date] = 1 * (avg < raw[date])
    ha = dict()
    with open('ha.csv') as data:
        for line in data:
            line = line.strip()
            fields = line.split(',')
            date = fields[-1]
            hao = fields[0]
            hac = fields[3]
            ha[date] = 1 * (hao < hac)
    zzs = dict()
    with open('zzs.csv') as data:
        for line in data:
            line = line.strip()            
            fields = line.split(',')
            date = fields[0]        
            level = fields[1]
            kind = fields[2]
            zzs[date] = level + ',' + kind
    so = dict()
    with open('so.csv') as data:
        for line in data:
            line = line.strip()            
            fields = line.split(',')
            date = fields[0]        
            so[date] = 1 * (float(fields[-1]) > float(fields[-2])) # binary (above or below)
    rsi = dict()
    with open('rsi.csv') as data:
        for line in data:
            line = line.strip()            
            fields = line.split(',')
            date = fields[0]        
            value = float(fields[-1])
            rsi[date] = int(value) // 20 # [0, 100] discretized to five levels [0, 4]
    ms = dict()                                                      
    with open ('macd_sma.csv') as data:
        for line in data:                
            if 'macd' in line:
                line = line.strip()                
                fields = line.split(',')
                date = fields[0]        
                value = float(fields[-2])
                ms[date] = 1 * (value > 0) # binary (positive or negative)
    me = dict()                                                      
    with open ('macd_ema.csv') as data:
        for line in data:                
            if 'macd' in line:
                line = line.strip()                
                fields = line.split(',')
                date = fields[0]        
                value = float(fields[-2])
                me[date] = 1 * (value > 0) # binary (positive or negative)
    complete = set(raw.keys()) & set(ha.keys()) & set(zzs.keys()) & set(so.keys()) & set(rsi.keys()) & set(ms.keys()) & set(me.keys())
    for w in windows:
        complete = complete & set(sma[w].keys())
        complete = complete & set(ema[w].keys())
    indicators = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['HA,ZZS-level,ZZS-kind,SO,RSI,MACD-SMA,MACD-EMA']
    for td in horizons:
        for thr in thresholds:
            with open(f'char_{td}_{thr}.csv', 'w') as output:
                hdr = ','.join(indicators) + ',label,c1,c2,c3'
                print(f'Date,{hdr}', file = output)
                semaphore = None
                for date in sorted(list(complete)):
                    baseline = float(raw[date])
                    skip = False
                    semaphore = zzs[date] if date in zzs else semaphore
                    beginning = datetime.datetime.strptime(date, fmt)
                    passed = 0
                    counter = 1
                    while passed < td:
                        current = beginning + datetime.timedelta(days = counter)
                        horizon = current.strftime(fmt)
                        counter += 1
                        if current > final: # out of data range
                            horizon = None
                            break
                        if horizon in raw:
                            passed += 1
                    if horizon is not None:
                        later = raw[horizon]
                        perc = 100 * ((float(later) - baseline) / baseline) 
                        magnitude = 1 * (fabs(perc) >= thr)
                        sign = 1 * (perc > 0)
                        # three classes
                        # significant increase = 2
                        # significant decrease = 0
                        # neither 1
                        forecast = 2 if magnitude and sign else 0 if magnitude and not sign else 1
                        classes = '1,0,0' if forecast == 0 else '0,1,0' if forecast == 1 else '0,0,1'
                        
                        ss = ','.join([str(sma[w][date]) for w in windows])
                        es = ','.join([str(ema[w][date]) for w in windows])      
                        print(f'{date},{ss},{es},{ha[date]},{semaphore},{so[date]},{rsi[date]},{ms[date]},{me[date]},{forecast},{classes}', file = output)
                    
    print(f'Characterization concluded after {time() - start} seconds')
