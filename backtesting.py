import backtrader as bt
from backtrader_func import * 
import lagtestV2 as lg 

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000.0)
cerebro.addstrategy(TestStrategy)


# get and add data feed 
dataframe = lg.get_coin_by_name_eod("BTC",start=1)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)
cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)