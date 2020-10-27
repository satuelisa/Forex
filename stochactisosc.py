closing = []
low = []
high = []
dates = []
with open('daily.dat') as data:
    for line in data:
        data = line.split()
        if len(data) > 0:
            dates.append(data[-1])
            closing.append(float(data[-2]))
            assert closing[-1] > 0 
            high.append(float(data[-3]))
            low.append(float(data[-4]))
        else:
            dates.append(None)
            closing.append(None)
            high.append(None)
            low.append(None)
l = 14
d = 4
window = []
missing = 0
threshold = 48
output = False
for t in range(l - 1, len(closing)):
    date = dates[t]
    if date is not None:
        lowwin = [l for l in low[(t - l + 1):(t + 1)] if l]
        if len(lowwin) > 2: # at least two data points were present
            lw = min(lowwin)
            highwin = [h for h in high[(t - l + 1):(t + 1)] if h]
            hw = max(highwin)
            if hw != lw:
                curr = 100 * (closing[t] - lw) / (hw - lw)
                window.append(curr)
                if len(window) > d:
                    window.pop(0)
                print(dates[t], curr, sum(window) / len(window))
                output = True
        else:
            missing += 1            
    else:
        missing += 1
        if missing > threshold:
            if output:
                print('  ') # break lines for missing data
                output = False
            missing = 0
            

