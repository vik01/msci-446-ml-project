from ast import increment_lineno
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

data = pd.read_csv('project_work\\airline-passenger-traffic.csv')
data.columns = ['Month', 'Passengers']
data['Month'] = pd.to_datetime(data['Month'], format='%Y-%m')
data = data.set_index('Month')
print(data.head())

# Show the data
data.plot(figsize=(20, 4))
plt.grid
plt.legend(loc='best')
plt.title('Airline Passenger Traffic')
plt.show(block=False)

# Show the missing values by linear interpolation
data = data.assign(Passengers_Linear_Interpolation=data.Passengers.interpolation(method='linear'))
data[['Passengers_Linear_Interpolation']].plot(figsize = (20,4))
plt.grid
plt.legend(loc='best')
plt.title('Airline Passenger Traffic: Linear Interpolation')
plt.show(block=False)


data['Passengers'] = data['Passengers_Linear_Interpolation']
data.drop(columns = ['Passengers_Linear_Interpolation'], inplace = True)

# box plot
import seaborn as sns
fig = plt


# histogram plot
fig = data.Passengers.hist(figsize = (20, 5))

from pylab import rcParams
import statsmodels.api as sm

# Additive
rcParams['figure.figsize'] = 22, 24
decomposition = sm.tsa.seasonal_decompose(data.Passengers, model = 'additive')
fig = decomposition.plot()
plt.show()

# Multiplicative
rcParams['figure.figsize'] = 22, 24
decomposition = sm.tsa.seasonal_decompose(data.Passengers, model = 'Multiplicative')
fig = decomposition.plot()
plt.show()

# Divide data into training = 120 data point, and testing = rest of data
train_set = 120
train = data[0:train_set]
test = data[train_set:]

# Simple Moving Average (SMA) Method
y_hat_sma = data.copy()
ma_window = 12
y_hat_sma['sma_forecast'] = data['Passengers'].rolling(ma_window).mean()
y_hat_sma['sma_forecast'][train_set:] = y_hat_sma['sma_forcast'][train_set-1]
plt.figure(figsize = (20, 5))
plt.grid()
plt.plot(train['Passengers'], label = 'Train')
plt.plot(test['Passengers'], label = 'Test')
plt.plot(y_hat_sma['sma_forecast'], label = 'Simple Moving Average on Data')
plt.legend(loc = 'best')
plt.title('Simple Moving Average')
plt.show

# Calculate error values
from sklearn.metrics import mean_squared_error
rmse = np.sqrt(mean_squared_error(test['Passengers'], y_hat_sma['sma_forecast'[train_set:]])).round(2)
mape = np.round(np.mean(np.abs(test['Passengers'] - y_hat_sma['sma_forecast'[train_set:]]) / test['Passengers']) * 100, 2)
results = pd.DataFrame({'Method':['Simple Moving Average Forecast'], 'MAPE': [mape], 'RMSE':[rmse]})
results = results[['Method', 'RMSE', 'MAPE']]
results

# exponential smoothing
def exponential_smoothing(series, alpha):
    result = [series[0]]
    for n in range(1, len(series)):
        result.append(alpha*series[n] + (1 - alpha)*result[n-1])
    return result

y_hat_exp = data.copy()
y_hat_exp['exp_forecast'] = exponential_smoothing(data['Passengers'], 0.1)
y_hat_exp['exp_forecast'][train_set:] = y_hat_exp['exp_forecast'][train_set - 1]
plt.figure(figsize = (20, 5))
plt.grid()
plt.plot(train['Passengers'], label = 'Train')
plt.plot(test['Passengers'], label = 'Test')
plt.plot(y_hat_sma['sma_forecast'], label = 'Exponential Smoothing on Data')
plt.legend(loc = 'best')
plt.title('Exponential Smooting')
plt.show


# Winter's Method
data.index.freq = 'MS' # monthly frequency
m = 12 
alpha = 1/(2*m)

from statsmodel.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
data['HWES1'] = SimpleExpSmoothing(data['Passengers']).fit(smoothing_level = alpha, optimized = False, use_brute = True).fittedvalues
plt.grid()
plt.plot(test['Passengers'], label = 'Passengers')
plt.plot(data['HWES1'], label = 'HWES1')
plt.legend(loc = 'best')
plt.title('Holt Winter Single Exponential Smoothing')
plt.show


# on both additive and multiplicative trend
data['HWES2_ADD'] = ExponentialSmoothing(data['Passengers'], trend = 'add', seasonal = 'add').fit().fittedvalues
data['HWES2_MUL'] = ExponentialSmoothing(data['Passengers'], trend = 'mul', seasonal = 'mul').fit().fittedvalues


