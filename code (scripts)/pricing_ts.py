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
ev_price = pd.read_csv('ev_pricing_transformed2.csv')
ev_price.head()

# create ts df and ensure date is datetime
ev_price1 = ev_price[['Date', 'Average EV Price']]
ev_price1.head()
ev_price1.dtypes
ev_price1['Date'] = pd.to_datetime(ev_price1['Date'])
ev_price1.dtypes

ev_price_ts = ev_price1
ev_price_ts

ev_price_ts.set_index('Date',inplace=True)
ev_price_ts.head()

# plot ts data to see trends
ev_price_ts.plot()
plt.show()

# rolling stats to see variation in mean and stdev
timeseries = ev_price_ts['Average EV Price']
timeseries.rolling(12).mean().plot(label='12 Month Rolling Mean')
timeseries.rolling(12).std().plot(label='12 Month Rolling Std')
timeseries.plot()
plt.legend()
plt.show()

# ets decomposition - show trends, seasonality, residuals
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ev_price_ts['Average EV Price'], period=12)  
figure = plt.figure()  
figure = decomposition.plot()  
figure.set_size_inches(15, 8)
plt.show()

# perform dickey fuller test (adf)
from statsmodels.tsa.stattools import adfuller
test_result = adfuller(ev_price_ts['Average EV Price'])
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
ev_price_ts['Price First Difference'] = ev_price_ts['Average EV Price'] - ev_price_ts['Average EV Price'].shift(1)
check_adf(ev_price_ts['Price First Difference'].dropna())

# plot stationary set 
ev_price_ts['Price First Difference'].plot()
plt.show()

# autocorrelation
from statsmodels.graphics.tsaplots import plot_acf
fig_first = plot_acf(ev_price_ts['Price First Difference'].dropna())
plt.show()

# perform ARIMA model
model = sm.tsa.statespace.SARIMAX(ev_price_ts['Average EV Price'],order=(0,1,0), seasonal_order=(1,1,1,12))
ARIMAresult = model.fit()
print (ARIMAresult.summary())

# model performance
ev_price_ts['model_performance'] = ARIMAresult.predict(start = 24, end= 36, dynamic= True)  
ev_price_ts[['Average EV Price', 'model_performance']].plot(figsize= (12,8))
plt.show() 
# Future date prediction 
forecast_values = ARIMAresult.forecast(steps=15)
print(forecast_values)
forecast_values.index = pd.date_range(start=ev_price_ts.index[-1], periods=15, freq='Y')

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(ev_price_ts.index, ev_price_ts['Average EV Price'], label='Actual')
ax.plot(forecast_values.index, forecast_values, label='Forecast')
ax.set_xlabel('Year')
ax.set_ylabel('Average EV Price')
ax.set_title('Average EV Price Forecast for Next 15 Years')
ax.legend()
plt.show()
