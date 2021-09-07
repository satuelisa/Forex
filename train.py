import numpy as np
import pandas as pd
from time import time
from sys import argv, stderr
from collections import defaultdict

from frlearn.neighbours import FRONEC
from frlearn.utils.owa_operators import strict
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

from characterize import horizons, thresholds

# rewritten from https://fuzzy-rough-learn.readthedocs.io/en/stable/_modules/frlearn/neighbours/preprocessors.html#FRFS
# to gain access to selected attributes

from frlearn.base import Preprocessor
from frlearn.neighbours.neighbour_search import KDTree, NNSearch
from frlearn.utils.np_utils import fractional_k, remove_diagonal
from frlearn.utils.owa_operators import OWAOperator, invadd, deltaquadsigmoid
from frlearn.utils.t_norms import lukasiewicz

class FRFS(Preprocessor):
    def __init__(self, n_features=None, owa_weights: OWAOperator = deltaquadsigmoid(0.2, 1), t_norm=lukasiewicz):
        self.n_features = n_features
        self.owa_weights = owa_weights
        self.t_norm = t_norm

    def process(self, X, y):
        scale = np.std(X, axis=0)
        scale = np.where(scale == 0, 1, scale)
        X_scaled = X / scale
        R_a = np.minimum(np.maximum(1 - np.abs(X_scaled[:, None, :] - X_scaled), 0), y[:, None, None] != y[:, None])
        POS_A_size = self._POS_size(R_a)
        selected_attributes = np.full(X.shape[-1], False)
        remaining_attributes = set(range(X.shape[-1]))
        best_size = 0
        condition = (lambda: np.sum(selected_attributes) < self.n_features) if self.n_features else (lambda: best_size < POS_A_size)
        while condition():
            best_size = 0
            for i in remaining_attributes:
                candidate = selected_attributes.copy()
                candidate[i] = True
                candidate_size = self._POS_size(R_a[..., candidate])
                if candidate_size > best_size:
                    best_size = candidate_size
                    new_attribute = i
            selected_attributes[new_attribute] = True
            remaining_attributes.remove(new_attribute)
        return selected_attributes

    def _POS_size(self, R_a):
        R = self.t_norm(R_a, axis=-1)
        return np.sum(self.owa_weights.soft_min(1 - R, k=fractional_k(1), axis=-1))

# rewriting ends

dataset = argv[1]
above = 0.8
replicas = 5
windows = [3, 5, 7, 14, 21]
full = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['H-A', 'ZZS-level', 'ZZS-kind', 'SO', 'RSI', 'MACD-SMA', 'MACD-EMA']

with open('header.tex', 'w') as hdr:
    print('\\begin{{tabular}}{{|l|ll|rr|{}|r|rr|}}\n\\hline'.format('c' * len(full)), file = hdr)
    print('\multirow{2}{*}{Data set} & \multirow{2}{*}{{\\bf H}} & \multirow{2}{*}{{\\bf T}} & \\multicolumn{2}{|c|}{{\\bf Score}} & '\
          + ' & '.join([f'\\sr \\multirow{{2}}{{*}}{{\\rotatebox{{90}}{{{label}}}}}' for label in full]), \
          '& \\multirow{2}{*}{\#} & \multicolumn{2}{|c|}{Runtime} \\\\\n', file = hdr)
    print('& & $\\min$ & $\\max$ & ' + ' & '.join([f'' for label in full]), \
          '& & $\mu$ & $\sigma$ \\\\\n\hline', file = hdr)

with open('footer.tex', 'w') as ftr:
      print('\\hline\n\\end{tabular}', file = ftr)    

total = 0
usage = defaultdict(int)
for horizon in horizons:
    for change in thresholds:
        scores = []
        times = []
        uses = defaultdict(int)
        for replica in range(replicas):
            total += 1
            start = time()
            data = pd.read_csv(f'char_{horizon}_{change}.csv')
            cols = list(data.columns)
            cols.remove('Date')
            for exclude in argv[2:]:
                cols = list(filter(lambda x: exclude not in x, cols))
            indicators = [i for i in filter(lambda x: 'HT-' not in x, cols)]
            classes = [i for i in filter(lambda x: 'HT-' in x, cols)]
            training, testing = train_test_split(data, test_size = 0.3)
            trainData = training[indicators].to_numpy()
            trainLabels = np.column_stack((training[classes[0]], training[classes[1]]))      
            scalarLabels = np.asarray([int(f'{row[0]}{row[1]}', 2) for row in trainLabels])
            preproc= FRFS()
            selected = preproc.process(trainData, scalarLabels)
            trainData = trainData[:, selected]
            for pos in range(len(selected)):
                if selected[pos]:
                    i = indicators[pos]
                    uses[i] += 1
            classifier = FRONEC(k = 10, Q_type = 1, R_d_type = 1)
            model = classifier.construct(trainData, trainLabels)
            testData = testing[indicators].to_numpy()
            testData = testData[:, selected]
            pred = [f'{r[0]:.0f}{r[1]:.0f}' for r in np.rint(model.query(testData))]
            true = [f'{i}{j}' for  (i, j) in zip(testing[classes[0]],
                                                 testing[classes[1]])]
            f1 = f1_score(true, pred, average = 'micro')
            scores.append(f1)
            times.append(time() - start)
        avg = np.mean(times)
        sd = np.std(times)
        high = max(scores)
        low = min(scores)
        for i in uses:
            usage[i] += uses[i]
        if high >= above:
            print('{\sc ', dataset, '} &', horizon, '&', change, '&', f'{low:.2f} & {high:.2f} &', \
                  ' & '.join([str(uses[x]) for x in full]), \
                  f'& {len(data):,} & {avg:.2f} & {sd:.2f} \\\\')
print('{\sc ', dataset, '} & \\multicolumn{4}{|r|}{\\%} & ' \
      + ' & '.join([f'{100 * usage[x] / total:.0f}' for x in full]), \
      ' & \\multicolumn{3}{|l|}{total} \\\\')
