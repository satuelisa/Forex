from collections import defaultdict

total = 5 * 7 * 5 * 30 # 5 pairs, 7 horizons, 5 thresholds, 30 replicas

features = dict()
combos = [1, 2, 3]
for d in combos:
    features[d] = defaultdict(list)
    with open(f'bottom{d}.tex') as data:
        for line in data:
            fields = line.split(' & ')
            pos = 1
            for f in fields[2:-1]:
                features[d][pos].append(int(f))
                pos += 1


print('Indicator,Percentage,Experiment')
for f in range(1, 18):
    for d in combos:
        values = features[d].get(f, [])
        perc = 100 * sum(values) / total
        print(f'{f},{perc},{d}')

#1 89 1
#1 65 2
#1 4 3
#2 18 1
#2 13 2 
#2 26 3 
#3 7 1
#3 30 2
#3 47 3 
#4 6 1
#4 24 2
#4 65 3

            
