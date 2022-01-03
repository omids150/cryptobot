import lagtestV2 as lg

# transaktionsdauer 
# BTC = 10 min avg
# eth = 16 Sekunden und 5 Minuten.
main_coins = ["BTC","ETH","ADA","XRP","SOL"]

main_coins = lg.get_main_coins_eod(main_coins,start=20,interval="1m")

join_df = lg.joinTimeSeries(main_coins)

fig = lg.plot_chart(join_df)

fig = lg.addMovingAndStd_toPlot(fig,join_df)

fig = lg.plot_chartV2(coin_dict=main_coins, fig=fig)

fig.show()

peak_snyc,sorted_res,res =  lg.detect_leg_corr(main_coins["XRP"]["scaled_price"],join_df["scaled_price"])
lg.lag_plot(res,peak_snyc)

