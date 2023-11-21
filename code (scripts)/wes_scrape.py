# Import libraries
import os
from turtle import clear
from numpy import append
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import pandas as pd 


# Create an URL object
url = 'https://afdc.energy.gov/vehicle-registration?year=2021'
# Create object page
page = requests.get(url)
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')
# print(soup)
table1 = soup.find('table', id='vehicle_registration')
print(table1)
# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
 title = i.text
 print(i.text)
 headers.append(title)
evdata = pd.DataFrame(columns = headers)
evdata = evdata.drop('2021 Light-Duty Vehicle Registration Counts by State and Fuel Type', axis=1)
print(evdata)

# Create a for loop to fill mydata
for j in table1.find_all('tr')[1:]:
 row_data = j.find_all('td')
 row = [i.text for i in row_data]
 length = len(evdata)
 print(row)

#  evdata.loc[length] = row
 evdata = evdata.append(pd.Series(row, index=evdata.columns[:len(row)]), ignore_index = True)

evdata = evdata.dropna(how='all')
evdata = evdata.replace(r'\n','', regex=True)
print(evdata)
os.chdir(r'C:\Users\wesle\Documents\github\datascience\datascience_2\Project\Project_Deliverable-1-EV\data (scraped files)')
evdata.to_csv("ev.csv")