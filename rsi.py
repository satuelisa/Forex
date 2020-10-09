closing = []
dates = []
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        dates.append(data[-1])
        closing.append(float(data[-2]))
        assert closing[-1] > 0 
diff = [0]
curr = closing[0]
n = len(closing)
for t in range(1, n):
    new = closing[t]
    perc = 100 * (new - curr)/curr
    diff.append(perc)
    curr = new
l = 14
gain = [d if d > 0 else 0 for d in diff[:l]]
loss = [-d if d < 0 else 0 for d in diff[:l]]
assert len(gain) == l
ag = sum(gain) / l
al = sum(loss) / l
curr = 100 - (100 / (1 + (ag / l) / (al / l)))
for t in range(l, n):
    d = diff[t]
    cg = d if d > 0 else 0
    cl = -d if d < 0 else 0
    gain = [d if d > 0 else 0 for d in diff[(t - l):t]]
    loss = [-d if d < 0 else 0 for d in diff[(t - l):t]]
    assert len(gain) == l
    ag = sum(gain) / l
    al = sum(loss) / l    
    print(dates[t], 100 - (100 / (1 + ((l - 1) * ag + cg) / ((l - 1) * al + cl))))
