import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import optimizers

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# fix random seed for reproducibility
np.random.seed(7)
#load the dataset
dataset_path = os.path.join(DIR_PATH, 'data/test.csv')
dataframe = pd.read_csv(dataset_path,usecols=[1],engine='python')
#show
'''
plt.plot(dataframe)
plt.show()
'''
dataset = dataframe.values
dataset = dataset.astype('float32')
#normalize dataset
scaler = MinMaxScaler(feature_range=(0,1))
dataset = scaler.fit_transform(dataset)
#split into train and test sets
#67-33
train_size = int(len(dataset) * 2 / 3)
test_size = len(dataset) - train_size
#kieu [[],[]]
train, test = dataset[0:train_size,:], dataset[train_size: len(dataset),:]
#convert an array of values into dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [],[]
	for i in range (len(dataset) - look_back -1):
		a = dataset[i:(i+look_back),0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)
#reshape into X=t, Y=t+1
look_back = 5
trainX, trainY = create_dataset(train,look_back)# trainX=[[],[]] - trainY=[]
testX, testY = create_dataset(test,look_back)
#reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX,(trainX.shape[0],trainX.shape[1],1)) 
testX = np.reshape(testX,(testX.shape[0],testX.shape[1],1))
#create and fit the LSTM network
model = Sequential()
model.add(LSTM(4,input_shape=(look_back,1)))
model.add(Dense(1))
#gd
sgd = optimizers.SGD(lr=0.05)
model.compile(loss='mean_squared_error',optimizer='adam')#ban dau adam
model.fit(trainX,trainY,epochs=100,batch_size=1,verbose=2)
'''
#serialize model to json
model_json = model.to_json()
with open("forecast_lstm_sgd_1000.json", "w") as json_file:
	json_file.write(model_json)
#serialize weights to HDF5
model.save('forecast_lstm_sdg_1000.h5')
'''
print("ok")
#make prediction
trainPredict = model.predict(trainX) #[[],[],[]]
testPredict = model.predict(testX)
#invert predictions
trainPredict = scaler.inverse_transform(trainPredict) #[[],[]]
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
#calcualte root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0],trainPredict[:,0]))
print('Train score: %.2f RSME' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0],testPredict[:,0]))
print('Test score: %.2f RSME' % (testScore))
#shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
#shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
#plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()