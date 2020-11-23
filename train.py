import numpy as np
import pandas as pd
from time import time
from frlearn.neighbours import FRONEC
from frlearn.utils.owa_operators import strict
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

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

windows = [3, 5, 7, 14, 21]
full = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['H-A', 'ZZS-level', 'ZZS-kind']
from collections import defaultdict
uses = defaultdict(int)
print('\\begin{{tabular}}{{|ll|r|{}|rr|}}\n\\hline'.format('c' * len(full)))
print('{\\bf H} & {\\bf T} & {\\bf Score} & ' + ' & '.join([f'\\rotatebox{{90}}{{{label}}}' for label in full]), '& \# & $t$ \\\\\n\hline')
from characterize import horizons, thresholds
for horizon in horizons:
    for change in thresholds:
        start = time()
        data = pd.read_csv(f'char_{horizon}_{change}.dat', sep = ' ')
        cols = list(data.columns)
        cols.remove('Date')
        indicators = [i for i in filter(lambda x: 'HT-' not in x, cols)]
        classes = [i for i in filter(lambda x: 'HT-' in x, cols)]
        training, testing = train_test_split(data, test_size = 0.3)
        trainData = training[indicators].to_numpy()
        trainLabels = np.column_stack((training[classes[0]], training[classes[1]]))      
        scalarLabels = np.asarray([int(f'{row[0]}{row[1]}', 2) for row in trainLabels])
        used = set()
        preproc= FRFS()
        selected = preproc.process(trainData, scalarLabels)
        trainData = trainData[:, selected]
        for pos in range(len(selected)):
            if selected[pos]:
                i = indicators[pos]
                used.add(i)
                uses[i] += 1
        classifier = FRONEC(k = 10, Q_type = 1, R_d_type = 1)
        model = classifier.construct(trainData, trainLabels)
        testData = testing[indicators].to_numpy()
        testData = testData[:, selected]            
        pred = [f'{r[0]:.0f}{r[1]:.0f}' for r in np.rint(model.query(testData))]
        true = [f'{i}{j}' for  (i, j) in zip(testing[classes[0]],
                                             testing[classes[1]])]
        f1 = f1_score(true, pred, average = 'micro')
        print(horizon, ' & ', change, ' & ', f'{f1:.3f} &', ' & '.join(['\\incl' if x in used else '\\excl' for x in full]), f'& {len(data)} & {time() - start:.3f} \\\\')
    print('\\hline')
print('\\multicolumn{3}{|r|}{Times selected:} & '  + ' & '.join([str(uses[x]) for x in full]), ' &  & \\\\\n\\hline\n\\end{tabular}')
                                                                                                   
