import yfinance as yf
import plotly.express as px
import numpy as np

msft = yf.Ticker("MSFT")

ms = msft.history(period="max")
ms.reset_index(inplace=True)

fig = px.line(ms, x="Date", y="Close", title='Microsoft stock prices')
fig.show()


comps = {
    "MSFT": "Microsoft Corp.",
    "GOOG": "Google, Inc.",
    "ORCL": "Oracle Corp.",
    "IBM": "International Business Machines Corp.",
    "HPQ": "Hewlett-Packard Co.",
    "EMC": "EMC Corp.",
    "ADBE": "Adobe Systems, Inc.",
    "CRM": "Salesforce.com, Inc.",
    "VMW": "VMware, Inc.",
    "INTU": "Intuit Corp."
}


# https://aroussi.com/post/python-yahoo-finance
from pandas_datareader import data as pdr

import yfinance as yf
yf.pdr_override() 

def get_company_data(company):
    data = pdr.get_data_yahoo(company, start="2019-01-01", end="2019-12-31")
    data.reset_index(inplace=True)
    data['company'] = company
    data.rename(columns={'Close': 'price', 'Date': 'date'}, inplace=True)
    data = data[['date',  'company', 'price']]
    data['pct_change'] = data.price.pct_change()
    data['log_ret'] = np.log(data.price) - np.log(data.price.shift(1))
    return data

data_all = []
for company, name in comps.items():
    data = get_company_data(company)
    data_all.append(data)

import pandas as pd
prices = pd.concat(data_all)

fig = px.line(prices, x="date", y="log_ret", color='company')
fig.show()

cors = pd.pivot(prices, columns='company', values='log_ret').corr()
np.round(cors, 2)