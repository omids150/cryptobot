import backtrader as bt
from backtraider_func import * 
import lagtestV2 as lg 

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000000.0)
cerebro.addstrategy(TestStrategy)

# get coin data
dataframe = lg.get_coin_by_name_eod("ADA",start=1)
print(dataframe[:3])
dataframe = dataframe[:3].copy(deep=True)
data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)

# get and add data feed 
cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)