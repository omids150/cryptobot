import lagtestV2 as lg 

# coin_df = lg.get_coin_by_name_eod("BTC",start=120)

# lg.plot_chart(coin_df)

# print(coin_df)

main_coins = ["BTC","ETH","ADA","XRP","SOL"]

main_coins_df = lg.get_main_coins_eod(main_coins,start=15,interval="5m")

fig = lg.plot_chartV2(main_coins_df)

fig.show()