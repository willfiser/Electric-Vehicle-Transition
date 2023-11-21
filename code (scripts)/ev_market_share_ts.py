# read-in libraries
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import os 

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

# rolling stats to see variation in mean and stdev
timeseries = ev_ms_ts['EV Percent of Market Share']
timeseries.rolling(12).mean().plot(label='12 Month Rolling Mean')
timeseries.rolling(12).std().plot(label='12 Month Rolling Std')
timeseries.plot()
plt.legend()
plt.show()

# ets decomposition - show trends, seasonality, residuals
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ev_ms_ts['EV Percent of Market Share'], period=12)  
figure = plt.figure()  
figure = decomposition.plot()  
figure.set_size_inches(15, 8)
plt.show()

# perform dickey fuller test (adf)
from statsmodels.tsa.stattools import adfuller
test_result = adfuller(ev_ms_ts['EV Percent of Market Share'])
print ('ADF Test:')
labels = ['ADF Statistic','p-value','No. of Lags Used','Number of Observations Used']
for value,label in zip(test_result,labels):
    print(label+': '+str(value))
if test_result [1] <= 0.05:
    print ("Reject null hypothesis and data is stationary")
else:
    print ("Fail to reject H0 thereby data is non-stationary ")

# build adf function for further test of stationarity 
def check_adf(time_series):
    test_result = adfuller(time_series)
    print('ADF Test:')
    labels = ['ADF Statistic','p-value','No. of Lags Used','Number of Observations Used']
    for value,label in zip(test_result,labels):
        print (label+': '+str(value))
    if test_result [1] <= 0.05:
        print ("Reject null hypothesis and data is stationary")
    else:
        print ("fail to reject H0 and data is non-stationary ")

# data is seasonal - perform differencing
ev_ms_ts['Market Share First Difference'] = ev_ms_ts['EV Percent of Market Share'] - ev_ms_ts['EV Percent of Market Share'].shift(1)
check_adf(ev_ms_ts['Market Share First Difference'].dropna())

# plot stationary set 
ev_ms_ts['Market Share First Difference'].plot()
plt.show()

# autocorrelation
from statsmodels.graphics.tsaplots import plot_acf
fig_first = plot_acf(ev_ms_ts['Market Share First Difference'].dropna())
plt.show()

# perform ARIMA model
model = sm.tsa.statespace.SARIMAX(ev_ms_ts['EV Percent of Market Share'],order=(5,1,0), seasonal_order=(1,1,1,12))
ARIMAresult = model.fit()
print(ARIMAresult.summary())

# model performance
ev_ms_ts['model_performance'] = ARIMAresult.predict(start = 125, end= 143, dynamic= True)  
ev_ms_ts[['EV Percent of Market Share', 'model_performance']].plot(figsize= (12,8))
plt.show() 


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



