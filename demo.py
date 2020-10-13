from random import random
import datetime

def change(magnitude = 20):
    return -magnitude / 2 + magnitude * random()

simulate = False
if simulate:
    day = datetime.date.today()
    length = 150
    closing = 200 * random()
    for step in range(length): # day
        variation = [closing]
        for moment in range(24): # hour
            while True:
                new = variation[-1] + change()
                if new > 0:
                    break
            variation.append(new)
        opening = variation[0]
        closing = variation[-1]
        low = min(variation)
        high = max(variation)
        print(step, opening, low, high, closing, day)
        day += datetime.timedelta(days = 1)
else:
    from sys import argv # use a data file
    import datetime
    with open(argv[1]) as raw:
        step = 0
        raw.readline() # header
        data = [line for line in raw]
        prev = None
        for line in data:
            fields = line.split(',')
            date = fields.pop(0).split('-')
            y = int(date.pop(0))
            m = int(date.pop(0))
            d = int(date.pop(0))
            h = int(fields.pop(0).split(':')[0])
            date = datetime.date(y, m, d)
            hour = datetime.time(hour = h, minute = 0)
            t = datetime.datetime.combine(date, hour)
            bidOpen = float(fields.pop(0))
            bidHigh = float(fields.pop(0))
            bidLow = float(fields.pop(0))            
            bidClose = float(fields.pop(0))
            bidChange = float(fields.pop(0)) # ignored for now
            askOpen = float(fields.pop(0))
            askHigh = float(fields.pop(0))
            askLow = float(fields.pop(0))
            print(step, bidOpen, bidLow, bidHigh, bidClose, t.strftime('%Y-%m-%d-%H'))
            step += 1
            if prev is not None:
                skip = (t - prev).days * 24
                t += datetime.timedelta(hours = skip)
                print('  ') # blank lines for discontinuities in gnuplot
                step += skip
            prev = t
             
            
    
                    
