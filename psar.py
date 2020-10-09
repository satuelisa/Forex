# -*- coding: utf-8 -*-

# adapted from https://raw.githubusercontent.com/virtualizedfrog/blog_code/master/PSAR/psar.py
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def psar(barsdata, iaf = 0.02, maxaf = 0.2):
    length = len(barsdata)
    dates = list(barsdata['Date'])
    high = list(barsdata['High'])
    low = list(barsdata['Low'])
    close = list(barsdata['Close'])
    psar = close[0:len(close)]
    psarbull = [None] * length
    psarbear = [None] * length
    bull = True
    af = iaf
    ep = low[0]
    hp = high[0]
    lp = low[0]
    
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        
        reverse = False
        
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf
    
        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]
                    
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]

    return {"dates":dates, "high":high, "low":low, "close":close, "psar":psar, "psarbear":psarbear, "psarbull":psarbull}

if __name__ == "__main__":
    barsdata = pd.read_csv('demo.dat', sep=' ', header = None, names = ['Step', 'Open', 'Low', 'High', 'Close', 'Date'])
    # ascending dates are expected in the function
    result = psar(barsdata)
    t = result['dates']
    close = result['close']
    psarbear = result['psarbear']
    psarbull = result['psarbull']
    plt.figure(figsize = (9, 5))
    plt.plot(t, close)
    plt.plot(t, psarbull)
    plt.plot(t, psarbear)
    plt.xlabel('Time')
    plt.ylabel('Parabolic SAR')
    xmarks = [t[i] for i in range(0, len(t), 60)]
    plt.xticks(xmarks)
    plt.savefig('psar.png', dpi = 150)
