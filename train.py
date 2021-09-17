import numpy as np
import pandas as pd
from time import time
from sys import argv, stderr
from collections import defaultdict
from dtreeviz.trees import dtreeviz
from sklearn.tree import DecisionTreeClassifier 

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
above = 0.75
underline = 0.9
emphasize = 0.7
visthr = 0.95
goal = 5
attempts = 10
from avg import windows 
full = [f'SMA-{w}' for w in windows] + [f'EMA-{w}' for w in windows] + ['HA', 'ZZS-level', 'ZZS-kind', 'SO', 'RSI', 'MACD-SMA', 'MACD-EMA']
exclusion = argv[2:]
NA = '---'

verbose = True # activate more printouts

skip = set()
for f in full:
    for e in exclusion:
        if e in f:
            skip.add(f)
            break
print('% EXCL', ' '.join(skip))

with open('header.tex', 'w') as hdr:
    print('\\begin{{tabular}}{{|l|ll|rr|{}|r|rr|rr|}}\n\\hline'.format('c' * len(full)), file = hdr)
    print('\multirow{2}{*}{Data set} & \multirow{2}{*}{{\\bf H}} & \multirow{2}{*}{{\\bf T}} & \\multicolumn{2}{|c|}{{\\bf Score}} & '\
          + ' & '.join([f'\\sr \\multirow{{2}}{{*}}{{\\rotatebox{{90}}{{{label}}}}}' for label in full]), \
          '& \\multirow{2}{*}{\#} & Feature selection & Classification \\\\\n', file = hdr)
    print('& & & $\\min$ & $\\max$ & ' + ' & '.join([f'' for label in full]), \
          '& & $\mu$ & $\sigma$ & $\mu$ & $\sigma$ \\\\\n\hline', file = hdr)
    
with open('footer.tex', 'w') as ftr:
      print('\\hline\n\\end{tabular}', file = ftr)    

total = 0
usage = defaultdict(int)
first = True
dt = open('dtscores.txt', 'a')
for horizon in horizons:
    for change in thresholds:
        scores = []
        fstimes = []
        ctimes = []
        uses = defaultdict(int)
        data = pd.read_csv(f'char_{horizon}_{change}.csv')
        cols = list(data.columns)
        cols.remove('Date')
        for exclude in exclusion:
            cols = list(filter(lambda x: exclude not in x, cols))
        if first:
            print('% INCL', ' '.join(cols[:-1]))
            first = False
        indicators = [i for i in filter(lambda x: 'label' not in x, cols)]
        labels = cols[-1]
        best = (None, None, None)
        highscore = 0
        success = 0
        presence = np.bincount(data[labels])
        if len(presence) < 3 or min(presence) < 2: 
            print(f'% OMIT {horizon} {change} has {presence} class counts')
            continue
        if verbose:
            print(f'%%% Initiating replicas for {horizon} {change}: {presence}')
        for replica in range(attempts): # if technically splits could be made
            if verbose:
                print(f'%%% Replica {success}, goal is {goal}, attempt {replica}')
            if success >= goal: # we have enough
                break
            training, testing = train_test_split(data, test_size = 0.3)
            expected = [ l for l in testing[labels] ] # a simple list
            ptest = np.bincount(expected)
            ptrain = np.bincount(training[labels])
            if min(len(ptest), len(ptrain)) < 3:
                print(f'% SKIP {horizon} {change} has {ptest} {ptrain} class counts in a replica, {presence}')
                continue
            trainData = training[indicators].to_numpy()
            n = len(training)
            # the classifier wants a matrix, not a vector
            trainLabels = np.reshape(training[labels].to_numpy(), (n, 1))
            if verbose:
                print(f'%%% Selecting features for a {horizon}-{change} replica')
            start = time()
            preproc = FRFS()
            selected = preproc.process(trainData, trainLabels)
            fstimes.append(1000 * (time() - start)) # ms
            trainData = trainData[:, selected] # apply the result of the feature selection 
            if verbose:
                print(f'%%% Training a classifier for a {horizon}-{change} replica')            
            start = time()
            classifier = FRONEC(k = 10, Q_type = 1, R_d_type = 1)
            model = classifier.construct(trainData, trainLabels)
            ctimes.append(1000 * (time() - start)) # ms
            testData = testing[indicators].to_numpy()
            testData = testData[:, selected]
            if verbose:
                print(f'%%% Computing the score for a {horizon}-{change} replica')                        
            predicted = model.query(testData).flatten().tolist() # as a list
            variety = np.bincount(predicted)
            if len(variety) == 1 or min(variety) == 0:
                print(f'%%% REJECT single-class results', variety)
                continue
            success += 1 # a functional replica
            f1 = f1_score(expected, predicted, average = 'weighted')
            scores.append(f1)
            for pos in range(len(selected)): # update the usage counters
                if selected[pos]:
                    i = indicators[pos]
                    uses[i] += 1
            total += 1 # update the replica total            
            if f1 > highscore:
                highscore = f1
                fnames = []
                for pos in range(len(selected)):
                    if selected[pos]:
                        fnames.append(full[pos])
                best = (trainData, labels, testData, expected, fnames)
        # build and draw a decision tree for the best replica if requested on command line
        if 'dt' in argv and highscore >= visthr:
            (train, labels, test, expected, fnames) = best
            dt = DecisionTreeClassifier()
            model = dt.fit(train, labels)
            v = dtreeviz(dt, train, labels,
                         target_name = "prediction",
                         feature_names = fnames,
                         class_names = ['below threshold', 'decrease', 'increase'])
            v.save(f'{dataset}_{horizon}_{change}.svg')
            predicted = dt.predict(test)
            dtf1 = f1_score(expected, predicted, average = 'weighted')
            print(f'{dataset} {horizon} {change} dt {dtf1} frs {highscore}', file = dt) 
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
            print(f'{comment}{{\sc {dataset}}} & {horizon} & {change} & {l} & {h} &', \
                  ' & '.join([str(uses[x]) if x not in skip else NA for x in full]), \
                  f'& {len(data):,} & {fsavg:.2f} & {fssd:.2f} & {cavg:.2f} & {csd:.2f} \\\\')
dt.close()
if total > 0:
    print('{\sc ', dataset, '} & \\multicolumn{4}{|r|}{Feature frequency (\\%)} & ' \
          + ' & '.join([f'{100 * usage[x] / total:.0f}' if x not in skip else NA for x in full]), \
          ' & \\multicolumn{3}{|l|}{\\phantom{total}} \\\\')
