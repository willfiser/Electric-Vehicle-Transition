# read-in libraries
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os 
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from pandas import DataFrame
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

# set up working directory
dir = (r'/Users/willfiser/Documents/GitHub/project-deliverable-1-ev-power/data (scraped files)')
dir = (r'C:\Users\wesle\Documents\github\datascience\datascience_2\Project\project-deliverable-1-ev-power\data (scraped files)')
os.chdir(dir)

# read in data 
ev_ms = pd.read_csv('ev_market_share_transformed.csv')
ev_ms.head()

# create ts df and ensure date is datetime
ev_ms1 = ev_ms[['Date', 'EV Percent of Market Share']]
ev_ms1.head()
ev_ms1.dtypes
ev_ms1['Date'] = pd.to_datetime(ev_ms1['Date'])
ev_ms1.dtypes

ev_ms_ts = ev_ms1
ev_ms_ts

ev_ms_ts.set_index('Date',inplace=True)
ev_ms_ts.head()

# plot ts data to see trends
ev_ms_ts.plot()
plt.show()

# correlation
autocorrelation_plot(ev_ms_ts)
pyplot.show()

# fit model
ev_ms_ts.index = ev_ms_ts.index.to_period('M')
model = ARIMA(ev_ms_ts, order=(22,1,0))
model_fit = model.fit()
# summary of fit model
print(model_fit.summary())
# line plot of residuals
residuals = DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()
# density plot of residuals
residuals.plot(kind='kde')
pyplot.show()
# summary stats of residuals
print(residuals.describe())

# split into train and test sets
X = ev_ms_ts.values
size = int(len(X) * 0.70)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
# walk-forward validation
for t in range(len(test)):
 model = ARIMA(history, order=(5,1,0))
 model_fit = model.fit()
 output = model_fit.forecast()
 yhat = output[0]
 predictions.append(yhat)
 obs = test[t]
 history.append(obs)
 print('predicted=%f, expected=%f' % (yhat, obs))
# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
pyplot.plot(test, label = 'Actual Market Rate')
pyplot.plot(predictions, color='red', label = 'Forecasted Market Share')
pyplot.legend()
pyplot.title('Electric Vehicle Market Share Forecast vs Actuals')
pyplot.show()


# perform ARIMA model
model = sm.tsa.statespace.SARIMAX(ev_ms_ts['EV Percent of Market Share'],order=(5,1,0), seasonal_order=(1,1,1,12))
ARIMAresult = model.fit()
print(ARIMAresult.summary())

# Future date prediction 
forecast_values = ARIMAresult.forecast(steps=60)
print(forecast_values)
forecast_values.index = pd.date_range(start=ev_ms_ts.index[-1], periods=5*12, freq='M')

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(ev_ms_ts.index, ev_ms_ts['EV Percent of Market Share'], label='Actual')
ax.plot(forecast_values.index, forecast_values, label='Forecast')
ax.set_xlabel('Months')
ax.set_ylabel('EV Marketshare')
ax.set_title('Average EV Price Forecast for Next 5 Years')
ax.legend()
plt.show()

