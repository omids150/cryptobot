import pandas as pd
import requests 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import datetime as datetime

def get_coin_by_name(name,time="max"):
    # get coin by name 
    url = f"https://api.coingecko.com/api/v3/coins/{name}/market_chart?vs_currency=eur&days={time}&interval=minutly" # -> warum bekomme ich nur Tägliche daten  ?
    res = requests.request("GET", url)
    coin_df = pd.DataFrame(res.json()["prices"],columns=["ts","price"])
    coin_df["ts"] = pd.to_datetime(coin_df["ts"].div(1000.0), unit="s") # -> nicht ganz sicher ob das stimmt 
    coin_df.set_index("ts")

    # Use min max Scaler on coins 
    scaler = MinMaxScaler()
    price_array = np.array(coin_df["price"]).reshape(-1,1)

    # print(price_array)
    scaled_price = scaler.fit_transform(price_array)
    print(scaled_price)
    scaled_price = [float(i) for i in scaled_price] #-> problem 


    # coin_df["scaled_price"] = scaled_price[0]

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

def plot_chart(coin1 ,coin2=None ,Name=""):
    #plot two coins 
    fig = px.line(coin1, x="ts", y="scaled_price",title=Name)
    try:
        bool(coin2 != None )
    except:
        fig.add_trace(go.Scatter(x=coin2["ts"], y=coin2["scaled_price"]))
    fig.show()

###############################################################################################
####################### ACTUAL CODE 
###############################################################################################

#get bitcoin and etherium data 
# main_coin_dict = get_main_coins(time=30)
# btc_df = main_coin_dict["bitcoin"]
# eth_df = main_coin_dict["ethereum"]

#get coin to compare 
rand_coin = get_coin_by_name("decentraland",time=30)

#plot_chart(btc_df,rand_coin)

# print(btc_df)
# print(eth_df)