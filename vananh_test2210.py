import numpy as np
import pandas as pd
import re
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
'''
df = pd.read_csv('job_amount.csv', parse_dates = ['day'], index_col = ['day'])
df.head()
print(df)#amount va day k tren 1 dong???
print(df)
plt.xlabel('Date')
plt.ylabel('Number of air passengers')
#plt.plot(df)
#plt.show()
'''
def normalize_salary(salary_value):
    res = salary_value
    if re.match(r"^(((\d{1,3}([\.,]\d{3})+)|(\d+))|(\w*\d+))$", str(salary_value)) is not None:
        test = re.match(r"^(((\d{1,3}([\.,]\d{3})+)|(\d+))|(\w*\d+))$", str(salary_value))
        print(test)
        print("match")
        res = int(re.sub(r'.,', '', str(salary_value)))
    else:
        value_list = re.findall(r'\d+', salary_value)
        if len(value_list) > 0:
            res = int(value_list[-1]) * 1000000
    #print("normalize salary_value")
    #print(res)
    return res
x = normalize_salary("7.")
print(x)
#https://www.timviecnhanh.com/tuyen-nhan-vien-kcs-3035801.html 31/1/2015