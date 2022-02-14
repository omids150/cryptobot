#modules
import backtrader as bt
import backtrader.feeds as btfeeds

# fiels 
from btFunc import *
from EODapi import * 

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000000.0)
cerebro.addstrategy(TestStrategy)

main_coins = get_main_coins_eod()

for name,df in main_coins.items():
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data, name=name)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)