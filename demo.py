from random import random
import datetime

month = {'Jan' : 1,
         'Feb' : 2,
         'Mar' : 3,
         'Apr' : 4,
         'May' : 5,
         'Jun' : 6,
         'Jul' : 7,
         'Aug' : 8,
         'Sep' : 9, 
         'Oct' : 10,
         'Nov' : 11,
         'Dec' : 12}

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
        for line in data[::-1]: # the other way around
            fields = line.split(',')
            date = fields.pop(0).split()
            m = month[date.pop(0)]
            d = int(date.pop(0))
            y = int(date.pop(0))
            closing = float(fields.pop(0))
            opening = float(fields.pop(0))
            high = float(fields.pop(0))
            low = float(fields.pop(0))
            print(step, opening, low, high, closing, f'{y}-{m:02d}-{d:02d}')
            step += 1 if datetime.date(y, m, d).weekday() < 4 else 3 # skip Sat and Sun
            
            
    
                    
