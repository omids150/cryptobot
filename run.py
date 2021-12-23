import lagtest as lg 
rand_coin_name = "tezos" #name of rand coin to get 
time = 30

main_coin_dict = lg.get_main_coins(time=time)
btc_df = main_coin_dict["bitcoin"]
eth_df = main_coin_dict["ethereum"]

#get coin to compare 
rand_coin_df = lg.get_coin_by_name(rand_coin_name,time=time)

btc_df["price_vec"] = list(btc_df[["ts","scaled_price"]].to_records(index=False))
rand_coin_df["price_vec"] = list(rand_coin_df[["ts","scaled_price"]].to_records(index=False))

btc_df["price_vec"].corr(rand_coin_df["price_vec"].shift(0))