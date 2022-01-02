import lagtestV2 as lg

main_coins = ["BTC","ETH","ADA","XRP","SOL"]

main_coins = lg.get_main_coins_eod(main_coins,start=15,interval="1m")

join_df = lg.joinTimeSeries(main_coins)

print(join_df)

print(main_coins["BTC"])

#######

# btc = lg.get_coin_by_name_eod("BTC")

# print(btc[["timestamp","scaled_price"]])

# btc = lg.returnsAndStd(btc,rolling=True)

# fig = lg.plot_chart(btc,mode="markers")

# fig = lg.addMovingAndStd(fig,btc)

