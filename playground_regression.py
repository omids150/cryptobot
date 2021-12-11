import lagtest as lg

time = 60

# make regression (non-linear) of domient crypto currencies 
dominant_crypto_curr = ["bitcoin","ethereum","cardano","ripple","solana"]

main_coin_dict = lg.get_main_coins(names=dominant_crypto_curr,time=time)

lg.plot_chartV2(main_coin_dict,mode="markers")
# calculate std deviation to reg funtion 

# treade outliers 