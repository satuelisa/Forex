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
            complete = set(raw.keys()) & set(ha.keys()) & set(zzs.keys())
    for w in windows:
        complete.update(sma[w].keys())
        complete.update(ema[w].keys())
        latest = None

    from period import postpone
    from math import fabs
    
    indicators = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['H-A ZZS-level ZZS-kind']

    for td in horizons:
        for thr in thresholds:
            with open(f'char_{td}_{thr}.dat', 'w') as output:
                classes =  [f'HT-{td}-{thr}-above HT-{td}-{thr}-sign']
                print('Date ' + ' '.join(indicators + classes), file = output)
                latest = None
                for date in sorted(list(complete)):
                    baseline = float(raw[date])
                    forecasts = ''
                    skip = False
                    latest = zzs[date] if date in zzs else latest
                    if latest is not None:
                        later = raw.get(postpone(date, td), None)
                        if later is not None: # data for that day not available
                            perc = 100 * ((float(later) - baseline) / baseline) 
                            forecasts = f'{1 * (fabs(perc) >= thr)} {1 * (perc > 0)}'
                            print(date, ' '.join([str(sma[w][date]) for w in windows]), \
                                  ' '.join([str(ema[w][date]) for w in windows]), \
                                  ha[date], latest, forecasts, file = output)
