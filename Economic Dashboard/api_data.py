
import pandas as pd
import numpy as np 
import datetime as dt
from datetime import date, timedelta
from urllib.request import urlopen, Request
import requests
import json
import config
import yfinance as yf

pd.options.display.float_format = '{:,.2f}'.format

#pass ticker of the company

# Work
stock=input("Enter a stock ticker symbol: ").upper()
df = yf.download(tickers=stock,period='1d',interval='1m')

# Request Financial Data from API and load to variables

IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=400&apikey={config.api}').json()

BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&limit=400&apikey={config.api}').json()

CF = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=quarter&limit=400&apikey={config.api}').json()

Ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{stock}?limit=40&apikey={config.api}').json()

key_Metrics = requests.get(f'https://financialmodelingprep.com/api/v3/key-metrics/{stock}?limit=40&apikey={config.api}').json()

profile = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={config.api}').json()

millions = 1000#000

#Create empty dictionary and add the financials to it

financials = {}

# dates = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
#for item in range(0,17):

dates = [2023,2022,2021,2020,2019]
for item in range(5):
    
    financials[dates[item]] ={}

    #Key Metrics
    financials[dates[item]]['Mkt Cap'] = key_Metrics[item]['marketCap'] 
    financials[dates[item]]['Debt to Equity'] = key_Metrics[item]['debtToEquity']
    financials[dates[item]]['Debt to Assets'] = key_Metrics[item]['debtToAssets']
    financials[dates[item]]['Revenue per Share'] = key_Metrics[item]['revenuePerShare']
    financials[dates[item]]['NI per Share'] = key_Metrics[item]['netIncomePerShare']
# Income Statement
    financials[dates[item]]['Revenue'] = IS[item]['revenue'] / millions
    financials[dates[item]]['Gross Profit'] = IS[item]['grossProfit'] / millions
    financials[dates[item]]['R&D Expenses'] = IS[item]['researchAndDevelopmentExpenses']/ millions
    financials[dates[item]]['Op Expenses'] = IS[item]['operatingExpenses'] / millions
    financials[dates[item]]['Op Income'] = IS[item]['operatingIncome'] / millions
    financials[dates[item]]['Net Income'] = IS[item]['netIncome'] / millions
# Balance Sheet
    financials[dates[item]]['Cash'] = BS[item]['cashAndCashEquivalents'] / millions
    financials[dates[item]]['Inventory'] = BS[item]['inventory'] / millions
    financials[dates[item]]['Cur Assets'] = BS[item]['totalCurrentAssets'] / millions
    financials[dates[item]]['LT Assets'] = BS[item]['totalNonCurrentAssets'] / millions
    financials[dates[item]]['Int Assets'] = BS[item]['intangibleAssets'] / millions
    financials[dates[item]]['Total Assets'] = BS[item]['totalAssets'] / millions
    financials[dates[item]]['Cur Liab'] = BS[item]['totalCurrentLiabilities'] / millions
    financials[dates[item]]['LT Debt'] = BS[item]['longTermDebt'] / millions
    financials[dates[item]]['LT Liab'] = BS[item]['totalNonCurrentLiabilities'] / millions
    financials[dates[item]]['Total Liab'] = BS[item]['totalLiabilities'] / millions
    financials[dates[item]]['SH Equity'] = BS[item]['totalStockholdersEquity'] / millions
# Cash Flow Statement
    financials[dates[item]]['CF Operations'] = CF[item]['netCashProvidedByOperatingActivities'] / millions
    financials[dates[item]]['CF Investing'] = CF[item]['netCashUsedForInvestingActivites'] / millions
    financials[dates[item]]['CF Financing'] = CF[item]['netCashUsedProvidedByFinancingActivities'] / millions
    financials[dates[item]]['CAPEX'] = CF[item]['capitalExpenditure'] / millions
    financials[dates[item]]['FCF'] = CF[item]['freeCashFlow'] / millions
    financials[dates[item]]['Dividends Paid'] = CF[item]['dividendsPaid'] / millions

    #Income Statement Ratios
    financials[dates[item]]['Gross Profit Margin'] = Ratios[item]['grossProfitMargin']
    financials[dates[item]]['Op Margin'] = Ratios[item]['operatingProfitMargin']
    financials[dates[item]]['Int Coverage'] = Ratios[item]['interestCoverage']
    financials[dates[item]]['Net Profit Margin'] = Ratios[item]['netProfitMargin']
    financials[dates[item]]['Dividend Yield'] = Ratios[item]['dividendYield']

    #BS Ratios
    financials[dates[item]]['Current Ratio'] = Ratios[item]['currentRatio']
    financials[dates[item]]['Operating Cycle'] = Ratios[item]['operatingCycle']
    financials[dates[item]]['Days of AP Outstanding'] = Ratios[item]['daysOfPayablesOutstanding']
    financials[dates[item]]['Cash Conversion Cycle'] = Ratios[item]['cashConversionCycle']

    #Return Ratios

    financials[dates[item]]['ROA'] = Ratios[item]['returnOnAssets']
    financials[dates[item]]['ROE'] = Ratios[item]['returnOnEquity']
    financials[dates[item]]['ROCE'] = Ratios[item]['returnOnCapitalEmployed']
    financials[dates[item]]['Dividend Yield'] = Ratios[item]['dividendYield']

    #Price Ratios

    financials[dates[item]]['PE'] = Ratios[item]['priceEarningsRatio']
    financials[dates[item]]['PS'] = Ratios[item]['priceToSalesRatio']
    financials[dates[item]]['PB'] = Ratios[item]['priceToBookRatio']
    financials[dates[item]]['Price To FCF'] = Ratios[item]['priceToFreeCashFlowsRatio']
    financials[dates[item]]['PEG'] = Ratios[item]['priceEarningsToGrowthRatio']
    financials[dates[item]]['EPS'] = IS[item]['eps']
    financials[dates[item]]['EPS'] = IS[item]['eps']

#Transform the dictionary into a Pandas
fundamentals = pd.DataFrame.from_dict(financials,orient='columns')

 #Calculate Growth measures
fundamentals['CAGR'] = ((fundamentals[2022]/fundamentals[2021])**(1/4) - 1)
fundamentals['2023 growth'] = (fundamentals[2023] - fundamentals[2022] )/ fundamentals[2022]
fundamentals['2022 growth'] = (fundamentals[2022] - fundamentals[2021] )/ fundamentals[2021]
fundamentals['2021 growth'] = (fundamentals[2021] - fundamentals[2020] )/ fundamentals[2020]
fundamentals['2020 growth'] = (fundamentals[2020] - fundamentals[2019] )/ fundamentals[2019]

# Export to CSV
fundamentals.to_csv('fundamentals.csv')

real_time_price = requests.get(f'https://financialmodelingprep.com/api/v3/quote-short/{stock}?apikey={config.api}')
gen_fin_news = requests.get(f'https://financialmodelingprep.com/api/v4/stock-news-sentiments-rss-feed?page=0&apikey={config.api}')
stock_news = requests.get(f'https://financialmodelingprep.com/api/v3/stock_news?tickers={stock}&limit=50&apikey={config.api}')
#price target consensus
target_price_consensus = requests.get(f'https://financialmodelingprep.com/api/v4/price-target-consensus?symbol={stock}&apikey={config.api}')
#price target summary
price_target_summary = requests.get(f'https://financialmodelingprep.com/api/v4/price-target-summary?symbol={stock}&apikey={config.api}')
# target upgrades and downgrades
target_up_down = requests.get(f'https://financialmodelingprep.com/api/v4/upgrades-downgrades?symbol={stock}&apikey={config.api}')
# earnings
earnings = requests.get(f'https://financialmodelingprep.com/api/v3/historical/earning_calendar/{stock}?limit=80&apikey={config.api}')
# historical dividends
div_hist = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{stock}?apikey={config.api}')
# economic calender
econ_calendar = requests.get(f'https://financialmodelingprep.com/api/v3/economic_calendar?from=2023-01-01&to=2023-12-31&apikey={config.api}')
# company outlook USE INSTEAD OF PROFILE
company_outlook = requests.get(f'https://financialmodelingprep.com/api/v4/company-outlook?symbol={stock}&apikey={config.api}')
# stock grade
stock_grade = requests.get(f'https://financialmodelingprep.com/api/v3/grade/{stock}?limit=500&apikey={config.api}')
# quarterly analyst estimates
analyst_est = requests.get(f'https://financialmodelingprep.com/api/v3/analyst-estimates/{stock}?period=quarter&limit=30&apikey={config.api}')
# treasury rates
bond_rates = requests.get(f'https://financialmodelingprep.com/api/v4/treasury?from=2023-03-1&to=2023-05-10&apikey={config.api}')
# fed funds
fed_funds = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=federalFunds&from=2019-01-01&to=2023-05-10&apikey={config.api}')
# cpi
cpi = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=CPI&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# real GDP
real_gdp = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=realGDP&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# consumer sentiment
consumer_senti = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=consumerSentiment&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# durableGoods
dur_goods = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=durableGoods&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# smoothedUSRecessionProbabilities 
recession_prob = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=smoothedUSRecessionProbabilities &from=2019-10-10&to=2023-05-10&apikey={config.api}')
# 15YearFixedRateMortgageAverage
fifteen_fmort = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=15YearFixedRateMortgageAverage&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# 30YearFixedRateMortgageAverage
thirty_fmort = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=30YearFixedRateMortgageAverage&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# unemploymentRate
unem_rate = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=unemploymentRate&from=2019-10-10&to=2023-05-10&apikey={config.api}')
# retailSales
ret_sales = requests.get(f'https://financialmodelingprep.com/api/v4/economic?name=retailSales&from=2019-10-10&to=2023-05-10&apikey={config.api}')

df = pd.read_csv('fundamentals.csv',index_col=0)


# years
df20 = df['2020']
df21 = df['2021']
df22 = df['2022']
df23 = df['2023']

# Statement data
cash = df.loc['Cash']
cur_assets = df.loc['Cur Assets']
lt_assets = df.loc['LT Assets']
int_assets = df.loc['Int Assets']
total_assets = df.loc['Total Assets']
mkt_cap = df.loc['Mkt Cap']
de = df.loc['Debt to Equity']
da = df.loc['Debt to Assets']
rps = df.loc['Revenue per Share']
rev = df.loc['Revenue']
gp = df.loc['Gross Profit']
op_inc = df.loc['Op Income']
ni = df.loc['Net Income']
cur_lia = df.loc['Cur Liab']
lt_debt = df.loc['LT Debt']
lt_lia = df.loc['LT Liab']
tot_lia = df.loc['Total Liab']
sh_eq = df.loc['SH Equity']
cf_ops = df.loc['CF Operations']
cf_inv = df.loc['CF Investing']
cf_fin = df.loc['CF Financing']
fcf = df.loc['FCF']
div_paid = df.loc['Dividends Paid']
op_margin = df.loc['Op Margin']
int_cov = df.loc['Int Coverage']
npm = df.loc['Net Profit Margin']
div_yld = df.loc['Dividend Yield']
#Ratios
cur_ratio = df.loc['Current Ratio']
roa = df.loc['ROA']
roe = df.loc['ROE']
roce = df.loc['ROCE']
pe = df.loc['PE']
ps = df.loc['PS']
pb = df.loc['PB']
price_to_fcf = df.loc['Price To FCF']
peg = df.loc['PEG']
eps = df.loc['EPS']