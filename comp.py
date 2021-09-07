from collections import defaultdict

features = defaultdict(list)
combos = [1, 2, 3]:
for d in combos:
    with open(f'bottom{d}.tex') as data:
        for line in data:
            fields = line.split(' & ')
            pos = 1
            for f in fields:
                print(pos, f)
                features[pos].append(f)
                pos += 1
            quit()

for feature in range(1, 18):
    for d in combos:
        value = features[feature][d]
        print(d, value, feature)

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

            
