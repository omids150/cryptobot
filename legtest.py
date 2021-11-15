import yfinance as yf
import datetime 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

def get_pairs(ticker=None):
    if type(ticker) != str and ticker!= None:
        raise ValueError

    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2021, 11, 15)

    btc =  yf.download("BTC-USD", progress=True, actions=True,start=start, end=end)
    eth =  yf.download("ETH-USD", progress=True, actions=True,start=start, end=end)

    if ticker != None:
        other =  yf.download(ticker, progress=True, actions=True,start=start, end=end)
        otehr_df = pd.DataFrame(other)

    bitcoin_df = pd.DataFrame(btc)
    ethereum_df = pd.DataFrame(eth)

    return bitcoin_df,ethereum_df

bitcoin_df,ethereum_df = get_pairs()

