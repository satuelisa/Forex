import os
from sys import argv

def clean(formatted):
    formatted = formatted.replace('{', '')
    formatted = formatted.replace('}', '')
    formatted = formatted.replace('\\', '')
    formatted = formatted.replace('em', '')
    formatted = formatted.replace('sc', '')
    formatted = formatted.replace('%', '')
    formatted = formatted.replace('underline', '')
    return formatted.strip().lstrip()

def pos(thr, mag):
    if mag == '1': # small 
        return ['0.01', '0.02', '0.03', '0.04', '0.05'].index(thr) + 1
    elif mag == '2': # medium
        return ['0.1', '0.2', '0.3', '0.4', '0.5'].index(thr) + 6
    else: # large
        return ['1.0', '1.5', '2.0', '2.5', '3.0'].index(thr) + 11

print('Pair,Horizon,Magnitude,Position,Threshold,Low,High')
prefix = argv[1] + '_'
for filename in os.listdir('.'):
    if filename.startswith(prefix) and filename.endswith('.tex'):
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
                line = line.strip().split('&')
                currency = clean(line.pop(0))
                horizon = clean(line.pop(0))
                horizon = '6' if horizon == '10' else '7' if horizon == '15' else horizon
                threshold = clean(line.pop(0))
                magnitude = str(1 if '0.0' in threshold else 2 if '0.' in threshold else 3)
                position = str(pos(threshold, magnitude))
                # skip three counters
                line = line[3:]
                low = clean(line.pop(0))
                high = clean(line.pop(0))
                output = [currency, horizon, magnitude, position, threshold, low, high]
                print(','.join(output))
