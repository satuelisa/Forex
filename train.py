import numpy as np
import pandas as pd
from time import time
from random import choice
from sys import argv, stderr
from sklearn.utils import resample
from collections import defaultdict
from sklearn.tree import DecisionTreeClassifier 

from frlearn.neighbours import FRONEC
from frlearn.utils.owa_operators import strict
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

from characterize import horizons, thresholds

# rewritten from
# https://fuzzy-rough-learn.readthedocs.io/en/stable/_modules/frlearn/neighbours/preprocessors.html#FRFS
# to gain access to selected attributes in order to count the usage frequency

from frlearn.base import Preprocessor
from frlearn.neighbours.neighbour_search import KDTree, NNSearch
from frlearn.utils.np_utils import fractional_k, remove_diagonal
from frlearn.utils.owa_operators import OWAOperator, invadd, deltaquadsigmoid
from frlearn.utils.t_norms import lukasiewicz

class FRFS(Preprocessor):
    def __init__(self, n_features = None, owa_weights: OWAOperator = deltaquadsigmoid(0.2, 1), t_norm = lukasiewicz):
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
MINIMUM = 30
above = 0.7
underline = 0.9
emphasize = 0.7
visthr = 0.95
replicas = 30
ss = 50 # sample size for feature selection
from avg import windows 
full = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['HA', 'ZZS-level', 'ZZS-kind', 'SO', 'RSI', 'MACD-SMA', 'MACD-EMA']
exclusion = argv[2:]
NA = '---'

verbose = False # activate more printouts

skip = set()
for f in full:
    for e in exclusion:
        if e in f:
            skip.add(f)
            break
print('% EXCL', ' '.join(skip))

with open('header.tex', 'w') as hdr:
    print('\\begin{{tabular}}{{|l|rr|rrr|rrr|{}|r|rr|rr|}}\n\\hline'.format('c' * len(full)), file = hdr)
    print('\multirow{2}{*}{Currency pair} & \multirow{2}{*}{{\\bf H}} & \multirow{2}{*}{{\\bf T}}', \
          ' & \\multicolumn{3}{|c|}{{\\bf Frequency}} & \\multicolumn{3}{|c|}{{\\bf Score}} & ',\
          ' & '.join([f'\\sr \\multirow{{2}}{{*}}{{\\rotatebox{{90}}{{{label}}}}}' for label in full]), \
          ' & \\multirow{2}{*}{\#} & \multicolumn{2}{|p{14mm}|}{Feature selection} & \multicolumn{2}{|c|}{Model} \\\\\n', file = hdr)
    print('& & & $\\downarrow$ & $\\approx$ & $\\uparrow$ & $\\min$ & $\\max$ & \\% & ' + ' & '.join([f'' for label in full]), \
          ' & & $\\mu$ & $\\sigma$ & $\\mu$ & $\\sigma$ \\\\\n\hline', file = hdr)
    
with open('footer.tex', 'w') as ftr:
      print('\\hline\n\\end{tabular}', file = ftr)    

total = 0
usage = defaultdict(int)
first = True
for horizon in horizons:
    for change in thresholds:
        scores = []
        fstimes = []
        ctimes = []
        absent = []
        uses = defaultdict(int)
        data = pd.read_csv(f'char_{horizon}_{change}.csv')
        n = len(data)
        cols = list(data.columns)
        cols.remove('Date')
        for exclude in exclusion:
            cols = list(filter(lambda x: exclude not in x, cols))
        if first:
            print('% INCL', ' '.join(cols[:-4]))
            first = False
        features = cols[:-4] # the last four are the labels
        binary = cols[-3:] # the last three are the 0/1 for each class
        labels = cols[-4] # these are the raw labels 0, 1, 2
        freq = np.unique(data[labels], return_counts = True)
        counters = { v: c for (v, c) in zip(freq[0], freq[1]) }
        assert n == sum(counters.values())
        present = sum([c >= MINIMUM for c in counters.values()])
        assert n > ss
        if min(len(counters), present) < 2:
            print(f'% insufficient data for H{horizon} T{change}')
            continue # not enough data
        if verbose:
            print(f'%%% Selecting features for H{horizon} T{change} with {n} data points')
        for replica in range(replicas): # if technically splits could be made
            parts = []
            goal = n // present
            for label in [0, 1, 2]: # resample to balance the classes
                if label in counters: 
                    matches = data[data.label == label]
                    lm = len(matches)
                    if lm >= MINIMUM: # disregard the nearly-absent class instead of gross oversampling
                        part = resample(matches, replace = lm < goal, n_samples = goal)
                        parts.append(part)
            training, testing = train_test_split(pd.concat(parts), test_size = 0.3)
            expected = [ l for l in testing[labels] ] # a simple list
            trainData = training[features].to_numpy()
            start = time()
            preproc = FRFS() # very slow, perform on a subset
            sample = resample(training, replace = False, n_samples = ss)
            selected = preproc.process(sample[features].to_numpy(), \
                                       np.reshape(sample[labels].to_numpy(), (ss, 1)))
            fstimes.append(1000 * (time() - start)) # ms
            for pos in range(len(selected)): # update the usage counters
                if selected[pos]:
                    i = features[pos]
                    uses[i] += 1
            total += 1
            trainData = trainData[:, selected] # apply the result of the feature selection
            trainLabels = training[binary].to_numpy() # these are the vectors [c1, c2, c3]
            if verbose:
                print(f'%%% Training a classifier for H{horizon} T{change}')            
            start = time()
            classifier = FRONEC(k = 10, Q_type = 1, R_d_type = 1)
            model = classifier.construct(trainData, trainLabels)
            ctimes.append(1000 * (time() - start)) # ms
            testData = testing[features].to_numpy()
            testData = testData[:, selected]
            fuzzy = model.query(testData)
            predicted = []
            for i in range(len(expected)): # defuzz the results
                result = fuzzy[i]
                highest = max(result)
                if highest == 0:
                    predicted.append(3) # none of the classes matched
                else:
                    matches = [] # could be more than one
                    for p in range(len(binary)):
                        if result[p] == highest:
                            matches.append(p)
                    if expected[i] in matches:
                        predicted.append(expected[i]) # rule in favor when present
                    else:
                        predicted.append(choice(matches)) # draw at random if absent
            absent.append(100 * np.sum(predicted == 3) / len(predicted))
            f1 = f1_score(expected, predicted, average = 'weighted')
            scores.append(f1)
        if len(scores) > 0:
            fsavg = np.mean(fstimes)
            fssd = np.std(fstimes)
            cavg = np.mean(ctimes)
            csd = np.std(ctimes)            
            high = max(scores)
            low = min(scores)
            for i in uses:
                usage[i] += uses[i]
            comment = '' if high >= above else '%'
            h = f'{high:.2f}'
            if high >= underline:
                h = '\\underline{' + h + '}'
            l = f'{low:.2f}'
            if low < emphasize:
                l = '{\\em ' + l + '}'
            ma = np.mean(absent)
            abs = f'{ma:.2f}' if ma > 0 else '---'
            classcounts = ' & '.join([str(counters[i]) if i in counters else '---' for i in [0, 1, 2]])
            print(f'{comment}{{\sc {dataset}}} & {horizon} & {change} & {classcounts} & ', \
                  f'{l} & {h} & {abs} &', \
                  ' & '.join([str(uses[x]) if x not in skip else NA for x in full]), \
                  f'& {len(data):,} & {fsavg:.2f} & {fssd:.2f} & {cavg:.2f} & {csd:.2f} \\\\')
if total > 0:
    print('{\sc ', dataset, '} & \\multicolumn{9}{|r|}{Frequency of inclusion in feature selection (\\%)} & ' \
          + ' & '.join([f'{100 * usage[x] / total:.0f}' if x not in skip else NA for x in full]), \
          ' & \\multicolumn{5}{|l|}{\\phantom{total}} \\\\')
