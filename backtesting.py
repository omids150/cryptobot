import backtrader as bt
from backtraider_func import * 
import lagtestV2 as lg 

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000.0)
cerebro.addstrategy(TestStrategy)

# main_coins = ["BTC","ETH","ADA","XRP","SOL"]
# main_coins = lg.get_main_coins_eod(main_coins,start=30,interval="1m")
# join_df = lg.joinTimeSeries(main_coins)

# get and add data feed 
dataframe = lg.get_coin_by_name_eod("BTC",start=1)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)
cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)