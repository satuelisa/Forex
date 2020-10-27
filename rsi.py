closing = []
dates = []
with open('daily.dat') as data:
    for line in data:
        f = line.split()
        if len(f) > 0:
            dates.append(f[-1])
            closing.append(float(f[-2]))
            assert closing[-1] > 0
        else:
            dates.append(None)
            closing.append(None)
diff = [0]
curr = closing[0]
n = len(closing)
for t in range(1, n):
    new = closing[t]
    if curr is not None and new is not None:
        perc = 100 * (new - curr)/curr
        diff.append(perc)
    else:
        diff.append(None)
    if new is not None:
        curr = new
l = 14
gain, loss = [], []
t = 0
while len(gain) < l: 
    d = diff[t]
    if d is not None:
        gain.append(d if d > 0 else 0)
        loss.append(-d if d < 0 else 0)
    t += 1
ag = sum(gain) / l
al = sum(loss) / l
threshold = 1
missing = 0
output = False
curr = 100 - (100 / (1 + (ag / l) / (al / l)))
for t in range(t, n):
    d = diff[t]
    if d is None:
        missing += 1
        if missing > threshold:
            if output:
                print(' ')
                output = False
    else:
        cg = d if d > 0 else 0
        cl = -d if d < 0 else 0
        gain = [d if d > 0 else 0 for d in [v for v in diff[(t - l):t] if v]]
        loss = [-d if d < 0 else 0 for d in [v for v in diff[(t - l):t] if v]]
        assert len(gain) == len(loss)
        k = len(gain)
        if k > 2: # at least three
            ag = sum(gain) / k
            al = sum(loss) / k
            try:
                print(dates[t], 100 - (100 / (1 + ((k - 1) * ag + cg) / ((k - 1) * al + cl))))
                output = True
                missing = 0
            except: 
                continue
        else:
            missing += 1                
