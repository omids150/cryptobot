import pandas as pd
import requests

#key 8d661ff9196adcc59e493c20c375732a8e3a101f

def get_main_coins():
    #btc
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_btc = requests.request("GET", url)
    btc_df = pd.DataFrame(response_btc.json()["prices"],columns=["ts","price"])
    btc_df["ts"] = pd.to_datetime(btc_df["ts"])
    btc_df.set_index("ts")

    #eth
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_eth = requests.request("GET", url)
    eth_df = pd.DataFrame(response_eth.json()["prices"],columns=["ts","price"])
    eth_df["ts"] = pd.to_datetime(eth_df["ts"])
    eth_df.set_index("ts")

    return btc_df,eth_df

def avalable_currencyes():
    res = requests.request("GET","https://api.coingecko.com/api/v3/coins/list")
    res = res.json()
    return pd.DataFrame(res)

btc_df,eth_df = get_main_coins()
coin_list = avalable_currencyes()

