from numpy.lib.function_base import _calculate_shapes
import lagtestV2 as lg

main_coins = ["BTC","ETH","ADA","XRP","SOL"]


main_coins_df = lg.get_main_coins_eod(main_coins,start=15,interval="1m")

btc = main_coins_df["BTC"]

lg.calc_retuns(btc["scaled_price"])
