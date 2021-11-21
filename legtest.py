from matplotlib.text import OffsetFrom
import pandas as pd
import requests 
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import lag_Corr as lg
import matplotlib.pyplot as plt
import statsmodels.api as sm


def scaleMinMax(a):
    # use min max scaler 
    scaler = MinMaxScaler()

    price_array = np.array(a).reshape(-1,1)

    scaled_price = scaler.fit_transform(price_array)
    scaled_price = [float(i) for i in scaled_price] #-> problem 

    return scaled_price

def get_coin_by_name(name,time="max"):
    # get coin by name 
    url = f"https://api.coingecko.com/api/v3/coins/{name}/market_chart?vs_currency=eur&days={time}&interval=minutes" # -> warum bekomme ich nur Tägliche daten  ?
    res = requests.request("GET", url)
    coin_df = pd.DataFrame(res.json()["prices"],columns=["ts","price"])
    coin_df["ts"] = pd.to_datetime(coin_df["ts"].div(1000.0), unit="s") # -> nicht ganz sicher ob das stimmt 
    coin_df.set_index("ts")

    coin_df["scaled_price"] = scaleMinMax(coin_df["price"])

    return  coin_df 

def get_main_coins(names=["bitcoin","ethereum"],time="max"):

    coin_dict = {}

    for n in names: 
        coin_df = get_coin_by_name(n,time=time)
        coin_dict[n] = coin_df
    
    return coin_dict

def avalable_currencyes():
    # get all avalable coin on coingecko 
    res = requests.request("GET","https://api.coingecko.com/api/v3/coins/list")
    res = res.json()
    return pd.DataFrame(res)

def plot_chart(coin1,coinName1="" ,coin2=None ,coinName2=""):
    if show_plots == False:
        return

    #plot two coins 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=coin1["ts"], y=coin1["scaled_price"],name=coinName1))
    try:
        bool(coin2 != None )
    except:
        fig.add_trace(go.Scatter(x=coin2["ts"], y=coin2["scaled_price"],name=coinName2))
    fig.show()

###############################################################################################
####################### ACTUAL CODE ######################
###############################################################################################
show_plots= False

time = 30
rand_coin_name = "algorand" 

#get bitcoin and etherium data 
main_coin_dict = get_main_coins(time=time)
btc_df = main_coin_dict["bitcoin"]
eth_df = main_coin_dict["ethereum"]

#get coin to compare 
rand_coin_df = get_coin_by_name(rand_coin_name,time=time)

# plot time series
plot_chart(btc_df,"bitcoin",rand_coin_df,rand_coin_name)


#calculate cross correlation
corr1 = sm.tsa.stattools.ccf(btc_df["scaled_price"], rand_coin_df["scaled_price"], adjusted=False)
corr2 = sm.tsa.stattools.ccf(rand_coin_df["scaled_price"], btc_df["scaled_price"], adjusted=False)

print("max corr1",max(corr1))
print("max corr2",max(corr2))


if max(corr1) >= max(corr2):
    result = np.where(corr1 == max(corr1) )
else:
    result = np.where(corr2 == max(corr2))

print(corr1[result])
