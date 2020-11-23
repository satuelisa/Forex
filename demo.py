from random import random
import datetime

def change(magnitude = 20):
    return -magnitude / 2 + magnitude * random()

simulate = False
if simulate: # simulated daily data for testing
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
    from sys import argv, stderr # use a data file
    import datetime
    skipped = 0
    hours = False
    window = 24 # in hours (24 for daily data)
    if len(argv) > 2:
        window = int(argv[2])
        print(f'# {window}-hour data expected')
        hours = True
        midnight = datetime.time(hour = 0, minute = 0)
        wl = datetime.timedelta(hours = window)
    with open(argv[1]) as raw:
        raw.readline() # skip header
        start = None
        bidOpen = []
        for line in raw:
            fields = line.split(',')
            ds = (fields.pop(0)).split('-')
            try:
                y = int(ds.pop(0))
                m = int(ds.pop(0))
                d = int(ds.pop(0))
                o = float(fields.pop(0))
                h = float(fields.pop(0))
                l = float(fields.pop(0))
                c = float(fields.pop(0))
            except:
                skipped += 1
                continue
            date = datetime.date(y, m, d)
            if not hours: # daily data
                print(o, l, h, c, date.strftime('%Y-%m-%d')  + '-00')
            else:
                h = int(fields.pop(0).split(':')[0])                
                hour = datetime.time(hour = h, minute = 0)
                t = datetime.datetime.combine(date, hour)
                if start is None or (t - start) > wl:
                    start = t
                    if window == 24: # daily data cuts off at midnight
                        start = datetime.datetime.combine(date, midnight)
                    if len(bidOpen) > 0: # there was data
                        print(bidOpen[0], min(bidLow), max(bidHigh), bidClose[-1], t.strftime('%Y-%m-%d-%H'))
                    # reset the data collectors
                    opening = []
                    high = []
                    low = []
                    closing = []
                high.append(h)
                low.append(l)
                closing.append(c)
                opening.append(o)
        if skipped > 0:
            print(f'Skipped {skipped} lines with incomplete data', file = stderr)


             
            
    
                    
