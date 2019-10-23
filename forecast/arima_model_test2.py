from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
 
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')
 
#series = read_csv('shampoo.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
series = read_csv('it.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)
print(series.head())
#autocorrelation_plot(series) #xac dinh p 
#series.plot() #hien thi du lieu ban dau
X = series.values
#print(X)
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()

for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('predicted=%f, expected=%f' % (yhat, obs))
error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)


#forecast next_month

for i in range(3):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	history.append(yhat)
	print(yhat)

# plot so sanh kq thuc te va du doan
pyplot.plot(test)
pyplot.plot(predictions, color='red')

pyplot.show()
#1,1,2 739394.412
#5,1,0 739394.412
#2,1,2 739394.412
'''
[10338.3271918]
[11207.67682037]
[11983.31603315]
'''
'''
#mo hinh (1,2,1)
Test MSE: 736112.664
[10744.78826879]
[11978.1825128]
[13299.53132572]
'''