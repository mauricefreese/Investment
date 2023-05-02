import pandas as pd
import datetime
import numpy as np
import datetime as dt
import math
from urllib.request import urlopen, Request
import requests
import config

# https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
def income_statement_quarterly(stock,api,q):
    '''
    Grabs the company's income statement from the quarter you want

    :param stock: the company's ticker you want to look at
    :type stock: str

    :param api: your api key for financial modeling prep
    :type api: str

    :param q: the qarter number you want, starting at 1 for the most recent quarter, then 2 for the second most recent quarter, so on and so forth
    :type q: int
    '''
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{stock}?period=quarter&limit=400&apikey={api}').json()

    financials = {}
    
    financials[q] = {}
    
    financials[q]['Revenue'] = IS[q]['revenue'] 
    financials[q]['Gross Profit'] = IS[q]['grossProfit']
    financials[q]['Gross Profit Ratio'] = IS[q]['grossProfitRatio'] 
    financials[q]['R&D Expenses'] = IS[q]['researchAndDevelopmentExpenses']
    financials[q]['Op Expenses'] = IS[q]['operatingExpenses'] 
    financials[q]['Op Income'] = IS[q]['operatingIncome']
    financials[q]['Operating Income Ratio'] = IS[q]['operatingIncomeRatio'] 
    financials[q]['Net Income'] = IS[q]['netIncome']
    financials[q]['Net Income Ratio'] = IS[q]['netIncomeRatio']
    financials[q]['Cost of Revenue'] = IS[q]['costOfRevenue']
    financials[q]['Cost and Expenses'] = IS[q]['costAndExpenses']
    financials[q]['Interst Income'] = IS[q]['interestIncome']
    financials[q]['Interest Expense'] = IS[q]['interestExpense']
    financials[q]['Depreciation and Ammortization'] = IS[q]['depreciationAndAmortization']
    financials[q]['EBITDA'] = IS[q]['ebitda']
    financials[q]['EBITDA Ratio'] = IS[q]['ebitdaratio']
    financials[q]['Total Other Income Expenses Net'] = IS[q]['totalOtherIncomeExpensesNet']
    financials[q]['Income Before Tax'] = IS[q]['incomeBeforeTax']
    financials[q]['Income Before Tax Ratio'] = IS[q]['incomeBeforeTaxRatio']
    financials[q]['Income Tax Expense'] = IS[q]['incomeTaxExpense']
    financials[q]['EPS'] = IS[q]['eps']
    financials[q]['EPS Diluted'] = IS[q]['epsdiluted']
    financials[q]['Weighted Average Shares Out'] = IS[q]['weightedAverageShsOut']
    financials[q]['Weighted Average Shares Out - Diluted'] = IS[q]['weightedAverageShsOutDil']
    financials[q]['Income Satement Link'] = IS[q]['finalLink']

    income = pd.DataFrame.from_dict(financials,orient='columns')

    return print(income.head(25))









#BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{stock}?period=quarter&limit=400&apikey={api}').json()

#CF = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{stock}?period=quarter&limit=400&apikey={api}').json()

#Ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{stock}?limit=40&apikey={api}').json()

#key_Metrics = requests.get(f'https://financialmodelingprep.com/api/v3/key-metrics/{stock}?limit=40&apikey={api}').json()

#profile = requests.get(f'https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={api}').json()
