import pandas as pd
import requests 
import plotly.express as px
import plotly.graph_objects as go


def get_main_coins():
    # btc
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_btc = requests.request("GET", url)
    btc_df = pd.DataFrame(response_btc.json()["prices"],columns=["ts","price"])
    btc_df["ts"] = pd.to_datetime(btc_df["ts"])
    btc_df.set_index("ts")

    # eth
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_eth = requests.request("GET", url)
    eth_df = pd.DataFrame(response_eth.json()["prices"],columns=["ts","price"])
    eth_df["ts"] = pd.to_datetime(eth_df["ts"])
    eth_df.set_index("ts")

    return btc_df,eth_df

def get_coin_by_name(name):
    # get coin by name 
    url = f"https://api.coingecko.com/api/v3/coins/{name}/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    res = requests.request("GET", url)
    coin_df = pd.DataFrame(res.json()["prices"],columns=["ts","price"])
    coin_df["ts"] = pd.to_datetime(coin_df["ts"])
    coin_df.set_index("ts")
    return  coin_df 

def avalable_currencyes():
    # get all avalable coin 
    res = requests.request("GET","https://api.coingecko.com/api/v3/coins/list")
    res = res.json()
    return pd.DataFrame(res)

def plot_chart(coin1,coin2=None):
    fig = px.line(coin1, x="ts", y="price", title='Life expectancy in Canada')
    if coin2 != None: 
        fig.add_trace(go.Scatter(x=coin2["ts"], y=coin2["price"]))
    fig.show()

btc_df,eth_df = get_main_coins()
rand_coin = get_coin_by_name("decentraland")
print(rand_coin)
plot_chart(btc_df,rand_coin)