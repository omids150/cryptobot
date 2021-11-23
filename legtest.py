from os import terminal_size
from matplotlib.text import OffsetFrom
from numpy.core.arrayprint import printoptions
from numpy.core.fromnumeric import _searchsorted_dispatcher, sort
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
    url = f"https://api.coingecko.com/api/v3/coins/{name}/market_chart?vs_currency=eur&days={time}&interval=minutely%20" # DATEN NICHT SAUBER !!!
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
    fig.add_trace(go.Scatter(x=coin1["ts"], y=coin1["scaled_price"],name=coinName1,mode="markers"))
    try:
        bool(coin2 != None )
    except:
        fig.add_trace(go.Scatter(x=coin2["ts"], y=coin2["scaled_price"],name=coinName2,mode="markers"))
    fig.show()

def detect_leg_corr(p1,p2,lag):

    #Plot haängt von lag ab und x achse sind indexes in der liste 
    #DYNAMISCH AUSPROGRAMIIEREN
    res = {} 
    for l in range(-int(lag),int(lag+1)):
        res[l] = lg.crosscorr(p1,p2, l) 

    sorted_res = dict(sorted(res.items(), key=lambda item: item[1],reverse=True))
    peak_snyc = list(sorted_res.items())[0]

    if show_plots == True:
        f,ax=plt.subplots(figsize=(14,3))
        ax.plot(res.keys(),res.values())
        ax.axvline(0,color='k',linestyle='--',label='Center')
        ax.axvline(peak_snyc[0],color='r',linestyle='--',label='Peak synchrony')
        ax.set(title='lag between currencyes', xlabel='Offset',ylabel='Pearson r')


    plt.savefig("./myplot.jpg")
    
###############################################################################################
####################### ACTUAL CODE ######################
###############################################################################################

show_plots= True # render or dont render plots

time = 30
rand_coin_name = "algorand" 

if __name__=="__main__":    #get bitcoin and etherium data 
    main_coin_dict = get_main_coins(time=time)
    btc_df = main_coin_dict["bitcoin"]
    btc_df["scaled_price"] = btc_df["scaled_price"].shift(10)
    btc_df.dropna()
    eth_df = main_coin_dict["ethereum"]

    #get coin to compare 
    rand_coin_df = get_coin_by_name(rand_coin_name,time=time)

    # plot time series
    plot_chart(btc_df,"bitcoin",rand_coin_df,rand_coin_name)

    #detect logs 
    detect_leg_corr(btc_df["scaled_price"],rand_coin_df["scaled_price"],150)

