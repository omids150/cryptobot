import pandas as pd
import requests 
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import lag_Corr as lg
import matplotlib.pyplot as plt 
import logging

def scaleMinMax(a):
    # use min max scaler 
    scaler = MinMaxScaler()

    price_array = np.array(a).reshape(-1,1)

    scaled_price = scaler.fit_transform(price_array)
    scaled_price = [float(i) for i in scaled_price] #-> problem 

    return scaled_price

def clean_data(df1,df2):
    # bring dfs to same lenth if not already 

    if len(df1) > len(df2):
        df1 = df1.tail(len(df2))
        df1.reset_index()
    elif len(df1) < len(df2):
        df2 = df2.tail(len(df1))
        # df2.reset_index()
    elif len(df1) == len(df2):
        logging.info("no ajustment needed")
    else:
        raise Warning

    return df1,df2
    
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

def plot_chart(coin1,coinName1="" ,coin2=None ,coinName2="",mode="lines"):

    #plot two coins 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=coin1["ts"], y=coin1["scaled_price"],name=coinName1,mode=mode))
    try:
        bool(coin2 != None )
    except:
        fig.add_trace(go.Scatter(x=coin2["ts"], y=coin2["scaled_price"],name=coinName2,mode=mode))
    fig.show()

def detect_leg_corr(p1,p2,lag=100):
    #caluclate sycrony 
    res = {} 
    for l in range(-int(lag),int(lag+1)):
        res[l] = lg.crosscorr(p1,p2, l) 

    sorted_res = dict(sorted(res.items(), key=lambda item: item[1],reverse=True))
    peak_snyc = list(sorted_res.items())[0]

    return peak_snyc,sorted_res,res

def lag_plot(res,peak_snyc):
    f,ax=plt.subplots(figsize=(14,3))
    ax.plot(res.keys(),res.values())
    ax.axvline(0,color='k',linestyle='--',label='Center')
    ax.axvline(peak_snyc[0],color='r',linestyle='--',label='Peak synchrony')
    ax.set(title='lag between currencyes', xlabel='Offset',ylabel='Pearson r')

    plt.savefig("./myplot.jpg")

def calc_std(df):
    #      normal std        std with scaled prices 
    return df["price"].std(),df["scaled_price"].std()

def windowed_time_lagged_cross_correlation(p1,p2,lag,no_splits):

    # (to see if leader and folower change not nesserery)
    samples_per_split = len(p1)/no_splits

    for t in range(0, no_splits):
        spit_p1 = p1.loc[(t)*samples_per_split:(t+1)*samples_per_split]
    