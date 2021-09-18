import os
from sys import argv

expected = 7 * 15 * 15
limit = 30
below = {0: 0, 1: 0, 2: 0}
giant = 0
total = 0

for filename in os.listdir('.'):
    if filename.startswith(argv[1]) and filename.endswith('.tex'):
        with open(filename) as data:
            for line in data:
                if 'insufficient' in line:
                    continue
                if 'INCL' in line:
                    continue
                if 'EXCL' in line:
                    continue
                if 'Frequency' in line:
                    continue
                line = line.replace('---', '0')
                total += 1
                line = line.strip().split('&')[3:6]
                cases = 0
                for count in range(3):
                    if int(line.pop(0)) < limit:
                        below[count] += 1
                        cases += 1
                if cases > 1:
                    giant += 1
for v in below:
    c = below[v]
    print(v, c, 100 * c / expected)
missing = expected - total
print('uniclass', giant, giant / expected)
print('untrainable', missing, missing / expected)
