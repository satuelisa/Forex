import os

datasets = dict()
for filename in os.listdir('.'):
    if 'cor.' in filename and '.csv' in filename:
        dataset = filename.split('.')[1]
        if len(dataset) == 3:
            dataset = f'USD{dataset}'
        if dataset not in datasets:
            datasets[dataset] = dict()
        with open(filename) as data:
            for line in data:
                line = line.strip()
                fields = line.split(',')
                if '.ha.' in filename:
                    t = fields[-1]
                    if t not in datasets[dataset]: 
                        datasets[dataset][t] = dict()
                    HAO = float(fields.pop(0))
                    HAL = float(fields.pop(0))
                    HAH = float(fields.pop(0))
                    HAC = float(fields.pop(0))
                    datasets[dataset][t]['HA diff'] = str(HAC - HAO)
                elif '.avg.' in filename:
                    kind = fields.pop(0).upper()
                    window  = int(fields.pop(0))
                    t = fields.pop(0)
                    value = fields.pop(0)
                    if window == 7: # analyze only one each
                        if t not in datasets[dataset]: 
                            datasets[dataset][t] = dict()                                        
                        datasets[dataset][t][f'{kind} {window}'] = value
                elif '.macd.' in filename:
                    kind = fields.pop(0).upper()
                    t = fields.pop(0)
                    value = fields.pop(0)
                    if t not in datasets[dataset]: 
                        datasets[dataset][t] = dict()   
                    datasets[dataset][t][f'MACD {kind}'] = value
                elif '.so.' in filename:
                    t = fields.pop(0)
                    value = fields.pop(0)
                    if t not in datasets[dataset]: 
                        datasets[dataset][t] = dict()                    
                    datasets[dataset][t][f'SO'] = value
                elif '.rsi.' in filename:
                    t = fields.pop(0)
                    value = fields.pop(0)
                    if t not in datasets[dataset]: 
                        datasets[dataset][t] = dict()
                    datasets[dataset][t][f'RSI'] = value
                elif '.zz.' in filename:
                    t = fields.pop(0)
                    level = fields.pop(0)
                    kind = fields.pop(0)
                    if t not in datasets[dataset]: 
                        datasets[dataset][t] = dict()
                    datasets[dataset][t][f'ZZ level'] = level
                    datasets[dataset][t][f'ZZ kind'] = kind
                else:
                    print('WARNING: ignoring', filename)
expected = 1 + 2 + 2 + 1 + 1 + 2 # HA, SMA + EMA, MACDs, SO, RSI, and two ZZs
order = None
header = None
for dataset in datasets:
    first = True
    with open(f'{dataset}.combined.csv', 'w') as target:
        datasets[dataset] = datasets[dataset]
        for t in datasets[dataset]:
            data = datasets[dataset][t]
            k = len(data)
            if k == expected:
                if order is None:
                    order = list(data.keys())
                    header = ','.join(key for key in order)                    
                if first:
                    print(f't,{header}', file = target)
                    first = False
                d = ','.join(data[key] for key in order)
                print(f'{t},{d}', file = target)
