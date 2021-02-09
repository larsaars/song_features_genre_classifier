import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pickle as pkl
from ast import literal_eval

# read df, make genres to str lists and drop all empty genres lists then
df = pd.read_csv('datasets/genre_db2.csv', sep=';')
# df['genre'] = df.genre.apply(literal_eval)
df = df[df.genre.apply(lambda gen: len(gen)) != 0]

# print the header of the df
print(df.head())

# create text train split
train, test = train_test_split(df, test_size=0.2)
# create test and train x, y
# X is data, y is target
trainY, testY = train.genre, test.genre
trainX, testX = train.drop(columns=['genre']), test.drop(columns=['genre'])

# fit linear regression
model = RandomForestClassifier(n_estimators=100, verbose=1, n_jobs=3)
model.fit(X=trainX, y=trainY)

# dump model into file after generating
with open('models/model.pkl') as file:
    pkl.dump(model, file)

# print test score
print('score: %f' % model.score(X=testX, y=testY))
