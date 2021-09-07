from math import fabs
from sys import argv

values = []
prev = None
pip = {'EUR-USD': 0.0001, 'EUR-JPY': 0.01, 'EUR-CHF': 0.0001, 'USD-JPY': 0.01, 'CAD-USD': 0.0001}
span = 100
filename = argv[1]
pair = filename.split('/')[-1].split('.')[0]
with open(filename) as data:
    for line in data:
        data = line.split(',')
        if len(data) > 0: # skip blank lines
            curr = float(data[4]) # closing
            if prev is not None:
                diff = prev - curr
                change = diff // pip[pair]
                if change != 0: # there as a significant change (at least one PIP)
                    values.append(change)
            prev = curr


import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot

bins = [32, 64, 128]
threshold = 0.01
mu = np.mean(values) 
sigma = np.std(values)
fig, axs = plt.subplots(3, len(bins),  tight_layout = True, figsize = (12, 9))
for i in range(len(bins)):
    ax = axs[0, i]
    sns.distplot(values, hist = True, kde = True, bins = bins[i], color = 'gray',  hist_kws = {'edgecolor' : 'black'}, kde_kws = {'linewidth': 1, 'color': 'blue'}, ax = ax)
    ax.set_xlim((-1.1 * span, 1.1 * span))
    ax.set_ylim((0, 0.05))
    ax.set_ylabel('Density')
    ax.set_xlabel(f'Change in PIP ({bins[i]} bins)')
    x = np.linspace(-span, span, 100)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color = 'red')    
    qqplot(np.array(values), line = 's', ax = axs[1, i], marker = '.', color = 'gray')
    h = stats.relfreq(values, numbins = bins[i])
    xp = h.lowerlimit + np.linspace(0, h.binsize * h.frequency.size, h.frequency.size)
    ax = axs[2, i]
    y = []
    x = []
    j = 0
    for j in range(len(xp)):
        v = h.frequency[j]
        if v >= threshold:
            y.append(v)
            x.append(xp[j])
        j += i
    ax.set_xlim((-1.1 * span, 1.1 * span))
    ax.set_ylim((0, 0.7))
    ax.set_ylabel('Relative frequency')
    ax.set_xlabel(f'Change in PIP ({len(x)} significant bins)')        
    ax.bar(x, y, width = h.binsize)
    plt.savefig('movements.png', dpi = 150)
        


