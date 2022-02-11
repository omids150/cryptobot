import backtrader as bt
from backtraider_func import * 
import lagtestV2 as lg 

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000000.0)
cerebro.addstrategy(TestStrategy)

Time = 60

#get coin data
dataframe = lg.get_coin_by_name_eod("ADA",start=Time)

# get indicator data -> scaled prices 
ind = get_corr_data(start=Time)

# join data frames 
datafeed = dataframe.join(ind,how="outer")

# get and add data feed 
data = custemData(dataname=datafeed)
cerebro.adddata(data)

cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)