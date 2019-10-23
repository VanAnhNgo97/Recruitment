import numpy as np, pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import auto_arima
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})


data = pd.read_csv('it.csv', parse_dates = ['day'], index_col = ['day'])
#divide into train and validation set
train = data[:int(0.7*(len(data)))]
valid = data[int(0.7*(len(data))):]
#preprocessing (since arima takes univariate series as input)
#train.drop('day',axis=1,inplace=True)
#valid.drop('day',axis=1,inplace=True)
#plotting the data
train['amount'].plot()
valid['amount'].plot()
#building the model

model = auto_arima(train, trace=True, error_action='ignore', suppress_warnings=True)
model.fit(train)

forecast = model.predict(n_periods=len(valid))
print(forecast)
forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])
print(forecast)
#plot the predictions for validation set
plt.plot(train, label='Train')
plt.plot(valid, label='Valid')
#plt.plot(forecast, label='Prediction')
plt.show()