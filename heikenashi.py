from sys import argv
HAO = None
HAC = None
with open(argv[1]) as data:
    data.readline() # skip header row
    for line in data:
        data = line.split(',') # CSV
        if len(data) == 0 or 'null' in data: # no data or missing data
            continue
        date = data[0]
        opening = float(data[1])        
        low = float(data[3])
        high = float(data[2])
        closing = float(data[4])
        if HAO is None:
            HAO = opening
        if HAC is None:
            HAC = closing
        HAC = (opening + high + low + closing) / 4
        HAO = (HAO + HAC) / 2
        HAH = max(high, HAO, HAC)
        HAL = min(low, HAO, HAC)
        print(f'{HAO},{HAL},{HAH},{HAC},{date}')


