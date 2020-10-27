HAO = None
HAC = None
with open('daily.dat') as data:
    for line in data:
        data = line.split()
        if len(data) == 0:
            continue
        date = data[-1]
        opening = float(data[0])        
        low = float(data[1])
        high = float(data[2])
        closing = float(data[3])
        if HAO is None:
            HAO = opening
        if HAC is None:
            HAC = closing
        HAC = (opening + high + low + closing) / 4
        HAO = (HAO + HAC) / 2
        HAH = max(high, HAO, HAC)
        HAL = min(low, HAO, HAC)
        print(HAO, HAL, HAH, HAC, date)


