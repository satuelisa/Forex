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
        sma5[date] = avg < raw[date]
sma21 = dict()
with open('roll_21.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
        avg = fields[1]
        sma21[date] = avg < raw[date]
ha = dict()
with open('ha.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[-1].split('-')[:-1]) # remove the hour        
        hao = fields[0]
        hac = fields[3]
        ha[date] = hao < hac
zzd = dict()
with open('zzs_daily.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour        
        level = fields[1]
        kind = fields[2]
        zzd[date] = level + kind
zz4 = dict()
with open('zzs_fourhour.dat') as data:
    for line in data:
        fields = line.split()
        date = '-'.join(fields[0].split('-')[:-1]) # remove the hour
        level = fields[1]
        kind = fields[2]        
        if date not in zz4:
            zz4[date] = '' 
        zz4[date] += level + kind # concatenate

complete = list(set(raw.keys()) & set(sma5.keys()) & set(sma21.keys()) & set(ha.keys()))
latest = None
for date in sorted(complete):
    latest = zzd[date] if date in zzd else latest
    if latest is not None:
        print(date, sma5[date], sma21[date], ha[date], latest, zz4.get(date, '44'))
