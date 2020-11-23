import pandas as pd
from random import random
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from sys import argv
raw = pd.read_csv(argv[1])
data = raw.head(500)
p = data['Close']
low = min(p)
high = max(p)
span = high - low
s = pd.Series(p)
n = len(s)
r = pd.Series([low + span * random() for i in range(n)])
# t = [pd.to_datetime((d + '-' + h), format = '%Y-%m-%d-%H:%M') for (d, h) in zip(data['Date'], data['Hour'])]
t = [pd.to_datetime((d), format = '%Y-%m-%d') for d in data['Date']]
fig, ax = plt.subplots(2, figsize = (8, 6))
ax[0].plot(t, r, color = 'blue', alpha = 0.3)
ax[0].plot(t, s, color = 'red')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Price')
xmarks = [t[i] for i in range(0, n, 60)]
plt.xticks(xmarks, rotation = 90)
lag = [l for l in range(0, n - 1)]
dac = [s.autocorr(l) for l in lag]
rac = [r.autocorr(l) for l in lag]
alpha = 0.05
ax[1].plot(lag, dac, color = 'red')
ax[1].plot(lag, rac, color = 'blue', alpha = 0.3)
ax[1].axhline(y = alpha, color = 'black', linestyle = '-', linewidth = 1, alpha = 0.5)
ax[1].axhline(y = -alpha, color = 'black', linestyle = '-', linewidth = 1, alpha = 0.5)
ax[1].set_xlabel('Lag')
ax[1].set_ylabel('Autocorrelation')
fig.tight_layout(pad = 1.0)
plt.savefig('autocor.png', dpi = 150)
