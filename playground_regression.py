import lagtestV2 as lg

main_coins = ["BTC","ETH","ADA","XRP","SOL"]

main_coins = lg.get_main_coins_eod(main_coins,start=15,interval="1m")

join_df = lg.joinTimeSeries(main_coins)

print(join_df)

fig = lg.plot_chart(join_df)

fig = lg.addMovingAndStd(fig,join_df)

print(main_coins)

fig = lg.plot_chartV2(coin_dict=main_coins, fig=fig)

fig.show()
