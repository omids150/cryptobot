import pandas as pd
import requests

#key 8d661ff9196adcc59e493c20c375732a8e3a101f

def get_main_coins():
    #btc
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_btc = requests.request("GET", url)    
    
    #eth
    url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=eur&days=max&interval=minutes%5"
    response_eth = requests.request("GET", url)
    

    btc_df = pd.DataFrame(response_btc.json()["prices"],columns=["ts","price"],index="prices")
    eth_df = pd.DataFrame(response_eth.json()["prices"],columns=["ts","price"])

    return btc_df,eth_df


btc_df,eth_df = get_main_coins()

print(btc_df)