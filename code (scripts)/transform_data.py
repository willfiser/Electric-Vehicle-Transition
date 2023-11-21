import pandas as pd
import os

# read in the pricing dataset
ev_pricing = pd.read_csv("data (scraped files)/EV Pricing.txt", delimiter="\t")
ev_pricing_t = ev_pricing.iloc[:, :5]

# transform data to int
ev_pricing_t['New Car Average'] = ev_pricing_t['New Car Average'].str[1:]
ev_pricing_t['New Car Average'] = ev_pricing_t['New Car Average'].str.replace(",", "")
ev_pricing_t['New Car Average'] = ev_pricing_t['New Car Average'].astype(int)

ev_pricing_t['Average EV Price'] = ev_pricing_t['Average EV Price'].str[1:]
ev_pricing_t['Average EV Price'] = ev_pricing_t['Average EV Price'].str.replace(",", "")
ev_pricing_t['Average EV Price'] = ev_pricing_t['Average EV Price'].astype(int)

# read in the sales dataset
ev_sales = pd.read_csv("data (scraped files)/EIA_EV_Data.txt", delimiter="\t")
ev_sales_t = ev_sales.copy()

# transform data to int
ev_sales_t['Stock of Evs'] = ev_sales_t['Stock of Evs'].str.replace(",", "")
ev_sales_t['Stock of Evs'] = ev_sales_t['Stock of Evs'].str.strip()
ev_sales_t['Stock of Evs'] = ev_sales_t['Stock of Evs'].astype(int)

# market share
ev_market_share = pd.read_csv("data (scraped files)/EV_Market_Share.txt", delimiter="\t")
ev_market_share1 = ev_market_share.copy()
ev_market_share1.dtypes

# transform market share data 
ev_market_share1['Date'] = pd.to_datetime(ev_market_share1['Date'])
ev_market_share1.dtypes
ev_market_share1.dropna(inplace=True)


# saving transformed files
ev_pricing_t.to_csv("data (scraped files)/ev_pricing_transformed.csv")
ev_sales_t.to_csv("data (scraped files)/ev_sales_transformed.csv")
ev_market_share1.to_csv("data (scraped files)/ev_market_share_transformed.csv")

