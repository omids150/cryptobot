import requests
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import stats as s

def get_coin_by_name_eod(name,interval="1m",start=30,end=time()):
    #start in days you want to look back 

    # convert start time 
    start = start * 24 * 60 * 60
    start = end - start
    
    url = f"https://eodhistoricaldata.com/api/intraday/{name}-USD.CC?api_token={cfg.api_token}&fmt=json&interval={interval}&from={start}&to={end}"

    response = requests.request("GET", url)
    coin_df = pd.DataFrame(response.json())
    coin_df = coin_df.rename(columns={"datetime": "ts"})
    coin_df = coin_df.drop(columns=["timestamp","gmtoffset"])

    coin_df["scaled_price"] = s.scaleMinMax(coin_df["close"])
    coin_df = coin_df.set_index("ts")
    coin_df.index = pd.to_datetime(coin_df.index)

    return coin_df

def get_main_coins_eod(names=["BTC","ETH","ADA","XRP","SOL"],interval="1m",start=30,end=time()):
    coin_dict = {}

    for n in names: 
        coin_df = get_coin_by_name_eod(n,interval=interval,start=start,end=end)
        coin_dict[n] = coin_df
    
    return coin_dict