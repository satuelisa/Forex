import numpy as np
import pandas as pd
from frlearn.neighbours import FRONEC
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def header(descr):
    f = descr.split('-')
    return ' & '.join(f[1:-1])

data = pd.read_csv('char.dat', sep = ' ', header = None)
indicators = ['SMA-5', 'SMA-21', 'H-A',
              'ZZS-24-level', 'ZZS-24-kind',
              'ZZS-4-level', 'ZZS-4-kind']
classes =  ['HT-short-small-above', 'HT-short-small-sign',
            'HT-short-intermediate-above', 'HT-short-intermediate-sign',
            'HT-short-large-above', 'HT-short-large-sign',
            'HT-medium-small-above', 'HT-medium-small-sign',
            'HT-medium-intermediate-above', 'HT-medium-intermediate-sign',
            'HT-medium-large-above', 'HT-medium-large-sign',
            'HT-long-small-above', 'HT-long-small-sign',
            'HT-long-intermediate-above', 'HT-long-intermediate-sign',
            'HT-long-large-above', 'HT-long-large-sign']
data.columns = ['Date'] + indicators + classes
training, testing = train_test_split(data, test_size = 0.3)
trainData = training[indicators].to_numpy()
testData = testing[indicators].to_numpy()
clf = FRONEC(k = 10, Q_type = 1, R_d_type = 1)

for pos in range(len(classes) // 2):
    trainLabels = np.column_stack((training[classes[2 * pos]],
                                   training[classes[2 * pos + 1]]))
    true = [f'{i}{j}' for  (i, j) in zip(testing[classes[2 * pos]],
                                         testing[classes[2 * pos + 1]])]
    model = clf.construct(trainData, trainLabels)
    pred = [f'{r[0]:.0f}{r[1]:.0f}' for r in np.rint(model.query(testData))]
    f1 = f1_score(true, pred, average = 'micro')
    print(header(classes[2 * pos]), '&', f'{f1:.3f}', '\\\\')
