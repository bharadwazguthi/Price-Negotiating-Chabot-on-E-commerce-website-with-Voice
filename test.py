import pandas as pd
import numpy as np
import cv2
import requests
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor

dataset = pd.read_csv("Dataset/model.csv")
dataset.fillna(0, inplace = True)

name = 'Dat Divi Engine Life Crop-top (3-Tone)'
products = dataset.loc[dataset['Name'] == name]
products = products.values
X = products[:,5:6]
Y = products[:,6:7]

sc = MinMaxScaler(feature_range = (0, 1))
X = sc.fit_transform(X)
Y = sc.fit_transform(Y)
svr_regression = SVR(C=1.0, epsilon=0.2)
#training SVR with X and Y data
svr_regression.fit(X, Y.ravel())
#performing prediction on test data
predict = svr_regression.predict(X)
predict = predict.reshape(predict.shape[0],1)
predict = sc.inverse_transform(predict)
predict = predict.ravel()
labels = sc.inverse_transform(Y)
labels = labels.ravel()
for i in range(len(predict)):
    print(str(labels[i])+" "+str(predict[i]))


svr_regression = KNeighborsRegressor(n_neighbors=2)
#training SVR with X and Y data
svr_regression.fit(X, Y.ravel())
#performing prediction on test data
predict = svr_regression.predict(X)
predict = predict.reshape(predict.shape[0],1)
predict = sc.inverse_transform(predict)
predict = predict.ravel()
labels = sc.inverse_transform(Y)
labels = labels.ravel()
for i in range(len(predict)):
    print(str(labels[i])+" "+str(predict[i]))


'''
sale = dataset['Sale price']
regular = dataset['Regular price']

price = []
negotiate = []

for i in range(len(sale)):
    if sale[i] != 0 and regular[i] != 0:
        price.append(regular[i])
        negotiate.append(sale[i])
    elif regular[i] == 0 and sale[i] == 0:
        price.append(20)
        negotiate.append(18)
    else:
        reg = (regular[i] / 100) * 10
        price.append(regular[i])
        negotiate.append(regular[i] - reg)
print(str(len(price))+" "+str(len(negotiate))+" "+str(dataset.shape))       
dataset.drop(['Sale price'], axis = 1,inplace=True)        
dataset.drop(['Regular price'], axis = 1,inplace=True)
dataset['Price'] = price
dataset['Negotiate'] = negotiate
dataset.to_csv("ecommerce.csv", index=False)


print(dataset['Sale price'])
print(dataset['Regular price'])


name = 'Dat Divi Engine Life Crop-top (3-Tone)'

products = dataset.loc[dataset['Name'] == name]
'''
