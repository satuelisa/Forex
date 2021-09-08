from collections import defaultdict

features = dict()
combos = [1, 2, 3, 4]
pairs = None
for d in combos:
    features[d] = defaultdict(list)
    with open(f'bottom{d}.tex') as data:
        c = 0
        for line in data:
            fields = line.split(' & ')
            pos = 1
            for f in fields[2:-1]:
                # get the average over the 30 replicas
                features[d][pos].append(int(f))
                pos += 1
            c += 1
        pairs = c if pairs is None else pairs
        assert pairs == c

print('Indicator,Percentage,Experiment')
for f in range(1, 18):
    for d in combos:
        values = features[d].get(f, [])
        perc = sum(values) / pairs
        assert perc >= 0 and perc <= 100
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

            
