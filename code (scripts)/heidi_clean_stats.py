import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ev_pricing_t = pd.read_csv("data (scraped files)/ev_pricing_transformed.csv")
ev_sales_t = pd.read_csv("data (scraped files)/ev_sales_transformed.csv")
ev_t = pd.read_csv("data (scraped files)/ev.csv")

### EV PRICING ###
ev_pricing_t.head()

#check missing values count
ev_pricing_t.isna().sum()

ev_pricing_t.shape

#drop missing values.
ev_pricing_t.dropna(inplace=True)

ev_pricing_t.shape

ev_pricing_t.dtypes

#need to remove %age signs from last 2 columns.
ev_pricing_t['New Car Price Change'] = ev_pricing_t['New Car Price Change'].str.rstrip("%").astype(float)
ev_pricing_t['EV Price Change'] = ev_pricing_t['EV Price Change'].str.rstrip("%").astype(float)

ev_pricing_t.dtypes
#also need to convert date to date type
# We can change this later.
ev_pricing_t['Date'] = pd.to_datetime(ev_pricing_t['Date'])

ev_pricing_t.dtypes

ev_pricing_t.describe(include = 'all')

#Charts
ev_pricing_t
import seaborn as sns
sns.scatterplot(data=ev_pricing_t, x="New Car Average", y="Average EV Price")
plt.show()

ev_pricing_t.corr()


### EV SALES ###
ev_sales_t.head()
ev_sales_t.dtypes

ev_sales_t.shape

#check missing values count
ev_sales_t.isna().sum()
#no missing values

#need to remove %age signs from EV Share of Sales.
ev_sales_t['EV Share of Sales'] = ev_sales_t['EV Share of Sales'].str.rstrip("%").astype(float)

ev_sales_t.dtypes
#years needs to be a different datatype
# We can change this later.
ev_sales_t.Year = pd.to_datetime(ev_sales_t.Year, format='%Y')

ev_sales_t.dtypes

ev_sales_t.describe(include = 'all')
#Charts and stuff, etc. FIXME


### EV PRICING ###
ev_t.head()

#check missing values count
ev_t.isna().sum()

#there is no missing data
ev_t.shape

ev_t.dtypes

#need to remove commas, strip the data, and change to numerical type.
ev_t_obj = ev_t.select_dtypes(['object'])
ev_t[ev_t_obj.columns] = ev_t_obj.apply(lambda x: x.str.strip())
ev_t[ev_t_obj.columns] = ev_t_obj.apply(lambda x: x.str.replace(",", ""))
ev_t.head()


#storing states so I can just ,erge it back on after I convert all to int data types in the remaining columns.
states = ev_t.iloc[:,0:2]
type(states)
states.head()
ev_t = ev_t.drop(ev_t.columns[1],axis=1)
ev_t_obj2 = ev_t.select_dtypes(['object'])
ev_t[ev_t_obj2.columns] = ev_t_obj2.apply(lambda x: x.astype(int))
type(ev_t)

ev_t = states.merge(ev_t, on='Unnamed: 0')

#drop redundant identifier of 1st column 'Unnamed: 0'
ev_t = ev_t.drop(ev_t.columns[0],axis=1)
ev_t.dtypes

ev_t.describe(include = 'all')
#Charts and stuff, etc. FIXME

import seaborn as sns
sns.boxplot(ev_t)
plt.xticks(rotation=25)
plt.show()
ev_t.Gasoline.max()
max_gas = ev_t[ev_t.Gasoline == 240699500]
max_gas

ev_t_states = ev_t.drop(axis=0,index=51)
ev_t_states

sns.boxplot(ev_t_states)
plt.xticks(rotation=25)
plt.show()

#max states for Gasoline and EV
ev_t_states.Gasoline.max()
max_gas_states = ev_t[ev_t.Gasoline == 30512600]
max_gas_states

ev_t_states['Electric (EV)'].max()
max_ev_states = ev_t[ev_t['Electric (EV)'] == 563100]
max_ev_states

#min states for Gasoline and EV
ev_t_states.Gasoline.min()
min_gas_states = ev_t[ev_t.Gasoline == 278900]
min_gas_states

ev_t_states['Electric (EV)'].min()
min_gas_states = ev_t[ev_t['Electric (EV)'] == 400]
min_gas_states

ev_t_states.corr()

ev_t_states.describe(include = 'all')


#Export the datafiles to CSVs in data folders

ev_t.to_csv("data (scraped files)/ev_t2.csv")
ev_pricing_t.to_csv("data (scraped files)/ev_pricing_transformed2.csv")
ev_sales_t.to_csv("data (scraped files)/ev_sales_transformed2.csv")

# market share stats
import os
dir = (r'/Users/willfiser/Documents/GitHub/project-deliverable-1-ev-power/data (scraped files)')
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

#describe 
ev_ms_ts.describe()