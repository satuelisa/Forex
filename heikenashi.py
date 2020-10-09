HAO = None
HAC = None
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        step = data[0]
        date = data[-1]
        opening = float(data[1])        
        low = float(data[2])
        high = float(data[3])
        closing = float(data[4])
        if HAO is None:
            HAO = opening
        if HAC is None:
            HAC = closing
        HAC = (opening + high + low + closing) / 4
        HAO = (HAO + HAC) / 2
        HAH = max(high, HAO, HAC)
        HAL = min(low, HAO, HAC)
        print(step, HAO, HAL, HAH, HAC, date)


