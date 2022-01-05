import backtrader as bt
from backtraider_func import * 
import lagtestV2 as lg 
import pandas as pd

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000.0)
cerebro.addstrategy(TestStrategy)

# get and add data feed 
dataframe = lg.get_coin_by_name_eod("BTC",start=2,interval="30m")

dataframe.index = pd.to_datetime(dataframe.index)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)
cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)