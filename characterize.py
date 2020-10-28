raw = dict()
with open('daily.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[-1].split('-')[:-1]) # remove the hour                
        closing = fields[3]
        raw[date] = closing
sma5 = dict()
with open('roll_5.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
        avg = fields[1]
        sma5[date] = 1 * (avg < raw[date])
sma21 = dict()
with open('roll_21.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
        avg = fields[1]
        sma21[date] = 1 * (avg < raw[date])
ha = dict()
with open('ha.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[-1].split('-')[:-1]) # remove the hour        
        hao = fields[0]
        hac = fields[3]
        ha[date] = 1 * (hao < hac)
zzd = dict()
with open('zzs_daily.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
        level = fields[1]
        kind = fields[2]
        zzd[date] = level + ' ' + kind
zz4 = dict()
with open('zzs_fourhour.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour
        level = fields[1]
        kind = fields[2]        
        zz4[date] = level + ' ' + kind # only the latest one

complete = list(set(raw.keys()) & set(sma5.keys()) & set(sma21.keys()) & set(ha.keys()))
latest = None

timedeltas = [1, 7, 14] # forecast horizon (days, hours, minutes)
thresholds = [2, 4, 6] # % change in closing price
from period import postpone
from math import fabs

for date in sorted(complete):
    latest = zzd[date] if date in zzd else latest
    if latest is not None:
        baseline = float(raw[date])
        forecasts = ''
        skip = False
        for td in timedeltas:
            later = raw.get(postpone(date, td), None)
            if later is not None:
                perc = 100 * ((float(later) - baseline) / baseline) 
                for thr in thresholds:
                     forecasts += f'{1 * (fabs(perc) >= thr)} {1 * (perc > 0)} '
            else:
                skip = True # incomplete data, uncharacterized
                break
        if not skip:
            print(date, sma5[date], sma21[date], ha[date], latest, zz4.get(date, '0 0'), forecasts.strip())
