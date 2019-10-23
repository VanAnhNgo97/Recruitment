import os,sys
import pymongo
import json
#from ..utils.utils import flatten_dict
from setting import *

#vananh
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bson.objectid import ObjectId
import bson
from count_job import JobUitl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

job_util = JobUitl()
data = job_util.statistic_category(8)
#df.to_csv('it.csv', sep='\t', encoding='utf-8')
#df = pd.DataFrame(data, columns = ['day','amount'])
#df.set_index('day').rolling(2).mean()
#chay ok xoa cot day and amount
#df = df.drop(df.columns[0],axis=1)
#print(df)
#df.to_csv('it.csv', sep='\t', encoding='utf-8')
#df.plot(kind='bar',x='day',y='amount',color='red')
#plt.xlabel('Day')
#plt.ylabel('Amount')
#plt.plot(df['day'],df['amount'])
#rolling mean
#rolling_mean = df.rolling(window = 12).mean()
#print(rolling_mean)
#plt.plot(df)#khong duoc???
#plt.show()
#plt.savefig('amount_line.png')
df = pd.read_csv('it.csv', parse_dates = ['day'], index_col = ['day'])
#print(df)
plt.xlabel('Date')
plt.ylabel('Number of air passengers')
#plt.plot(df)
rolling_mean = df.rolling(window = 12).mean()
rolling_std = df.rolling(window = 12).std()
#plt.plot(df, color = 'blue', label = 'Original')
#plt.plot(rolling_mean, color = 'red', label = 'Rolling Mean')
#plt.plot(rolling_std, color = 'black', label = 'Rolling Std')
#plt.legend(loc = 'best')
#plt.title('Rolling Mean & Rolling Standard Deviation')
#plt.show()
result = adfuller(df['amount'])
print('ADF Statistic: {}'.format(result[0]))
print('p-value: {}'.format(result[1]))
print('Critical Values:')
for key, value in result[4].items():
	print('\t{}: {}'.format(key, value))
df_log = np.log(df)
#plt.plot(df_log)
#plt.show()
#plt.show()
def get_stationarity(timeseries):
    # rolling statistics
    rolling_mean = timeseries.rolling(window=12).mean()
    rolling_std = timeseries.rolling(window=12).std()
    
    # rolling statistics plot
    original = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolling_mean, color='red', label='Rolling Mean')
    std = plt.plot(rolling_std, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    # Dickey–Fuller test:
    result = adfuller(timeseries['Passengers'])
    print('ADF Statistic: {}'.format(result[0]))
    print('p-value: {}'.format(result[1]))
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t{}: {}'.format(key, value))