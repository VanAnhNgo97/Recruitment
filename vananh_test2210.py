import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
'''
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
'''
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#ok
#df = pd.read_csv('AirPassengers.csv', parse_dates = ['date'], index_col = ['date'])
df = pd.read_csv('job_amount.csv', parse_dates = ['day'], index_col = ['day'])
df.head()
print(df)#amount va day k tren 1 dong???
print(df)
plt.xlabel('Date')
plt.ylabel('Number of air passengers')
#plt.plot(df)
#plt.show()