from legtest import *
import pandas as pd

time = 90 # how many days showld the history data go back
lag = 300

# get main coins to compare and calculate cross corrolation
main_coin_dict = get_main_coins(time=time)

btc_df = main_coin_dict["bitcoin"]
eth_df = main_coin_dict["ethereum"]

btc_df.iloc[1]["price"] = None 

print(btc_df.head(5)) 