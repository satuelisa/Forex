import pandas as pd
from sys import argv
from dtreeviz.trees import dtreeviz
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier 


data = pd.read_csv(argv[1])
cols = list(data.columns)
full = cols[1:-4] # the first one is the date and the last four are the labels
labels = cols[-4] # these are the raw labels (0, 1, 2)
names = []
for f in full:
    if f in argv or len(argv) < 3:
        names.append(f)
X = data[names]
y = data[labels]
print(names)

dt = DecisionTreeClassifier()
model = dt.fit(X, y)
v = dtreeviz(model, X, y,
             target_name = 'trend',
             feature_names = names,
             class_names = ['decrease', 'stable', 'increase'])
v.save('dt.svg')
print(f1_score(y, dt.predict(X), average = 'weighted'))

