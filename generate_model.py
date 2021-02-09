import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

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

# create the model
model = RandomForestClassifier(n_estimators=100, verbose=2, n_jobs=3)
# # create training time estimator
# estimator = Estimator(meta_algo='RF', verbose=3)
# # run the estimation
# estimation, lower_bound, upper_bound = estimator._estimate(algo=model, X=trainX, y=trainY)
# # print estimations
# print('estimated time to train:\nesimation: %f\nlower: %f\nupper: %f' % (estimation, lower_bound, upper_bound))
# fit linear regression
model.fit(X=trainX, y=trainY)

# dump model into file after generating
with open('models/model.pkl') as file:
    pkl.dump(model, file)

# print test score
print('score: %f' % model.score(X=testX, y=testY))
