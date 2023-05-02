from dash import Dash,html,dcc
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import talib as ta
from ta.trend import MACD 
from ta.momentum import StochasticOscillator 
import numpy as np 
from talib import abstract
import yfinance as yf
import mplfinance as fplt
import datetime as dt
from datetime import date, timedelta
import matplotlib.pyplot as plt
import seaborn as sns 
import math
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen, Request
import requests
import config
from plotly.subplots import make_subplots

# Intialize the app
app = Dash(__name__,external_stylesheets=dbc.themes.DARKLY)

# Work
stock=input("Enter a stock ticker symbol: ").upper()
df = yf.download(tickers=stock,period='1d',interval='1m')

# Moving Averages
df['20EMA']=ta.EMA(df['Close'],20)
df['5EMA']=ta.EMA(df['Close'],5)
ema_lines = df[['5EMA','20EMA']]

# RSI
df['RSI'] = ta.RSI(df['Close'],14)
RSI_col = df['RSI']
RSI = fplt.make_addplot(RSI_col)

# Support and Resistance
pivot_point = (df['High'] + df['Low'] + df['Close']) / 3

df['support_l1'] = (pivot_point *2) - df['High']
df['support_l2'] = pivot_point - (df['High'] - df['Low'])
df['resistance_l1'] = (pivot_point * 2) - df['Low'] 
df['resistance_l2'] = pivot_point + (df['High'] - df['Low'])

# MACD 
macd = MACD(close=df['Close'], 
            window_slow=26,
            window_fast=12, 
            window_sign=9)
# Stochastic
stoch = StochasticOscillator(high=df['High'],
                             close=df['Close'],
                             low=df['Low'],
                             window=14, 
                             smooth_window=3)


    # Declaring plotly figure (go)
fig = go.Figure()

fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                    vertical_spacing=0.01, 
                    row_heights=[0.5,0.1,0.2,0.2])
# Candlestick Chart
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'], 
                             showlegend=False))

#  20 Day Moving Average
fig.add_trace(go.Scatter(x=df.index,
                             y=df['20EMA'],
                             opacity=0.7,
                             line=dict(color='blue',width=2),
                             name = 'MA 20'))

# 5 day Moving Average
fig.add_trace(go.Scatter(x=df.index,
                             y=df['5EMA'],
                             opacity=0.7,
                             line=dict(color='orange',width=2),
                             name = 'MA 5'))

# adding a subplot 
# fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.5,0.1,0.2,0.2]) 

# Plot volume trace on 2nd row in our figure
colors = ['green' if row['Open'] - row['Close'] >= 0 
          else 'red' for index, row in df.iterrows()]
fig.add_trace(go.Bar(x=df.index, 
                     y=df['Volume'],
                     marker_color=colors
                     ), row=2, col=1)
# Plot MACD trace on 3rd row

colorsM = ['green' if val >= 0 
          else 'red' for val in macd.macd_diff()]
fig.add_trace(go.Bar(x=df.index, 
                     y=macd.macd_diff(),
                     marker_color=colorsM,
                    ), row=3, col=1)
fig.add_trace(go.Scatter(x=df.index,
                         y=macd.macd(),
                         line=dict(color='black', width=2)
                        ), row=3, col=1)
fig.add_trace(go.Scatter(x=df.index,
                         y=macd.macd_signal(),
                         line=dict(color='blue', width=1)
                        ), row=3, col=1)
# Plot stochastics trace on 4th row
fig.add_trace(go.Scatter(x=df.index,
                         y=stoch.stoch(),
                         line=dict(color='black', width=1)
                        ), row=4, col=1)
fig.add_trace(go.Scatter(x=df.index,
                         y=stoch.stoch_signal(),
                         line=dict(color='blue', width=1)
                        ), row=4, col=1)

# update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
fig.update_layout(height=900, width=1200, 
                  showlegend=False, 
                  xaxis_rangeslider_visible=False)

# Make the title dynamic to reflect whichever stock we are analyzing
fig.update_layout(
    title='Live Share Price: ' + str(stock),
    yaxis_title='Stock Price (USD Per Shares)'
)

# update y-axis label
fig.update_yaxes(title_text="Price", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)
fig.update_yaxes(title_text="MACD", showgrid=False, row=3, col=1)
fig.update_yaxes(title_text="Stoch", row=4, col=1)


fig.update_layout(
    xaxis=dict(
    rangeslider_visible=False,
    rangeselector_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label="15m", step="minute", stepmode="backward"),
            dict(count=45, label="45m", step="minute", stepmode="backward"),
            dict(count=1, label="HTD", step="hour", stepmode="todate"),
            dict(count=3, label="3h", step="hour", stepmode="backward"),
            dict(step="all")      
        ]), 
    )
))

fig.update_xaxes(matches='x')

fig.show()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)