import importlib
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
    fig.add_trace(go.Scatter(x=coin1["ts"], y=coin1["scaled_price"],name=coinName1,mode=mode))

    fig.show()

def plot_chartV2(coin_dict,mode="lines"):
    #plot dict of coins 
    fig = go.Figure()
    for coin in coin_dict.items():
        fig.add_trace(go.Scatter(x=coin[1]["ts"], y=coin[1]["scaled_price"],name=coin[0],mode=mode))

    fig.show()