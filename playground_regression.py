from numpy.lib.function_base import _calculate_shapes
from lagtest import calc_std, get_coin_by_name, plot_chart
import lagtestV2 as lg

main_coins = ["BTC","ETH","ADA","XRP","SOL"]

main_coins_df = lg.get_main_coins_eod(main_coins,start=15,interval="1m")



# btc = lg.get_coin_by_name_eod("BTC")

# btc = lg.returnsAndStd(btc,rolling=True)

# fig = lg.plot_chart(btc,mode="markers")

# fig = lg.addMovingAndStd(fig,btc)

# fig.show()