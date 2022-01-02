import pandas as pd
import requests 
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import config as cfg
from time import time
import lag_Corr as lg 
import matplotlib.pyplot as plt 


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

def addMovingAndStd_toPlot(fig,coin):
    fig.add_trace(go.Scatter(x=coin.index, y=coin["rolling"],line_color = "black",mode="lines"))
    upper = coin["rolling"]+coin["scaled_price_std"]
    lower = coin["rolling"]-coin["scaled_price_std"]

    fig.add_trace(go.Scatter(x=coin.index, y=upper,line_color = "#52A4F6",fill=None ,mode="lines"))
    fig.add_trace(go.Scatter(x=coin.index, y=lower,line_color = "#52A4F6" ,fill="tonexty",mode="lines"))

    return fig

def plot_chartV2(coin_dict,mode="lines",fig=None):
    #plot dict of coins 
    if fig == None:
        fig = go.Figure()

    for coin in coin_dict.items():
        fig.add_trace(go.Scatter(x=coin[1].index, y=coin[1]["scaled_price"],name=coin[0],mode=mode))

    return fig 

def returnsAndStd(coin,rolling = False,window = 300):
    coin["returns"] = coin["scaled_price"]-coin["scaled_price"].shift(1)
    coin["scaled_price_std"] = coin["scaled_price"].std()

    if rolling == True:
        coin["rolling"] = coin["scaled_price"].rolling(window).mean()

    return coin 
    
def joinTimeSeries(Dict,window=300):
    # this function also alters the orignial data frames!!!

    df = pd.DataFrame()

    for d in Dict.items():       
        scaled_price = d[1].copy(deep=True).drop(columns=['timestamp', 'gmtoffset',"open","high","close","low","volume"])
        join = scaled_price.rename(columns={"scaled_price": d[0]})
    
        df = df.join(join,how="outer")

    df["scaled_price"] = df.mean(axis=1)  # avrage price of all ticker in pool
    df = returnsAndStd(df,rolling=True,window=window)

    return df 

def detect_leg_corr(p1,p2,lag=100):
    #caluclate sycrony 
    # negativer lag p2 gibt p1 an  
    res = {} 
    for l in range(-int(lag),int(lag+1)):
        res[l] = lg.crosscorr(p1,p2, l) 

    sorted_res = dict(sorted(res.items(), key=lambda item: item[1],reverse=True))
    peak_snyc = list(sorted_res.items())[0]

    return peak_snyc,sorted_res,res

def lag_plot(res,peak_snyc,image_name="./myplot.jpg"):

    image_name = "./images/"+image_name

    f,ax=plt.subplots(figsize=(14,3))
    ax.plot(res.keys(),res.values())
    ax.axvline(0,color='k',linestyle='--',label='Center')
    ax.axvline(peak_snyc[0],color='r',linestyle='--',label='Peak synchrony')
    ax.set(title='lag between currencyes', xlabel='Offset',ylabel='Pearson r')

    plt.savefig(image_name)