closing = []
low = []
high = []
dates = []
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        dates.append(data[-1])
        closing.append(float(data[-2]))
        assert closing[-1] > 0 
        high.append(float(data[-3]))
        low.append(float(data[-4]))
l = 14
d = 3
window = []
for t in range(l - 1, len(closing)):
    lowwin = low[(t - l + 1):(t + 1)]
    assert len(lowwin) == l
    lw = min(lowwin)
    hw = max(high[(t - l + 1):(t + 1)])
    curr = 100 * (closing[t] - lw) / (hw - lw)
    window.append(curr)
    if len(window) > d:
        window.pop(0)
    print(dates[t], curr, sum(window) / len(window))


