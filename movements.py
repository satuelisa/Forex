from math import fabs

values = []
prev = None
pip = 0.0001 # EUR-USD
with open('demo.dat') as data:
    for line in data:
        data = line.split()
        if len(data) > 0: # skip blank lines
            curr = float(data[4]) # closing
            if prev is not None:
                diff = prev - curr
                change = diff // pip
                if change != 0: # there as a significant change (at least one PIP)
                    values.append(change)
            prev = curr

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

plt.xlabel('Change in PIPs in closing price')
plt.xlim((-100, 100))
plt.ylabel('Relative frequency')
y, x, p = plt.hist(values, density = True, bins = 30)
mu = np.mean(values) 
sigma = np.std(values)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.savefig('relative.png', dip = 150)
print(mu, sigma)
plt.clf()


from statsmodels.graphics.gofplots import qqplot
qqplot(np.array(values), line='s')
plt.savefig('qq.png')
