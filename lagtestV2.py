import importlib
from os import PRIO_PGRP
from typing import Dict
from numpy.core.arrayprint import printoptions
from numpy.core.fromnumeric import sort
import pandas as pd
import requests 
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import lag_Corr as lg
import matplotlib.pyplot as plt 
import logging
import seaborn as sns
import config as cfg
from time import time

from lagtest import windowed_time_lagged_cross_correlation 

def scaleMinMax(a):
    # use min max scaler to scale data into compareble prices 
    scaler = MinMaxScaler()

    price_array = np.array(a).reshape(-1,1)

    scaled_price = scaler.fit_transform(price_array)
    scaled_price = [float(i) for i in scaled_price] #-> problem 

    return scaled_price

def get_coin_by_name_eod(name,interval="1m",start=30,end=time()):
    #start in days you want to look back 

    # convert start time 
    start = start * 24 * 60 * 60
    start = end - start
    
    url = f"https://eodhistoricaldata.com/api/intraday/{name}-USD.CC?api_token={cfg.api_token}&fmt=json&interval={interval}&from={start}&to={end}"

    response = requests.request("GET", url)
    coin_df = pd.DataFrame(response.json())
    coin_df = coin_df.rename(columns={"datetime": "ts"})

    coin_df["scaled_price"] = scaleMinMax(coin_df["close"])
    coin_df = coin_df.set_index("ts")

    return coin_df

def get_main_coins_eod(names=["BTC","ETH"],interval="1m",start=30,end=time()):
    coin_dict = {}

    for n in names: 
        coin_df = get_coin_by_name_eod(n,interval=interval,start=start,end=end)
        coin_dict[n] = coin_df
    
    return coin_dict

def plot_chart(coin1,coinName1="",mode="lines"):
    #plot one coins 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=coin1.index, y=coin1["scaled_price"],name=coinName1,mode=mode))

    return fig

def addMovingAndStd(fig,coin):
    fig.add_trace(go.Scatter(x=coin.index, y=coin["rolling"],mode="lines"))
    upper = coin["rolling"]+coin["scaled_price_std"]
    lower = coin["rolling"]-coin["scaled_price_std"]

    fig.add_trace(go.Scatter(x=coin.index, y=upper, fill=None ,mode="lines"))
    fig.add_trace(go.Scatter(x=coin.index, y=lower,fill="tonexty",mode="lines"))

    return fig

def plot_chartV2(coin_dict,mode="lines"):
    #plot dict of coins 
    fig = go.Figure()
    for coin in coin_dict.items():
        fig.add_trace(go.Scatter(x=coin[1]["ts"], y=coin[1]["scaled_price"],name=coin[0],mode=mode))

    return fig 

# def calc_retuns(p):
#     return p-p.shift(1)

# def calc_std(p):
#     return p.std()

def returnsAndStd(coin,rolling = False,window = 300):
    coin["returns"] = coin["scaled_price"]-coin["scaled_price"].shift(1)
    coin["scaled_price_std"] = coin["scaled_price"].std()

    if rolling == True:
        coin["rolling"] = coin["scaled_price"].rolling(window).mean()

    return coin 
    
def joinTimeSeries(Dict,window=300):
    df = pd.DataFrame()

    for d in Dict.items():       
        scaled_price = d[1].drop(columns=['timestamp', 'gmtoffset',"open","high","close","low","volume"])
        Dict[d[0]] = scaled_price.rename(columns={"scaled_price": d[0]})
    
    for d in Dict.items():  
        df = df.join(d[1],how="outer")

    df["avg"] = df.mean(axis=1)
    df = returnsAndStd(df,rolling=True,window=window)

    return df 