import backtrader as bt
from backtraider_func import * 
import lagtestV2 as lg 

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000.0)
cerebro.addstrategy(TestStrategy)

dataframe = lg.get_coin_by_name_eod("BTC",start=1)

################
################
################

ind = get_corr_data(start=1)
# print(ind)
# print(dataframe)

datafeed = dataframe.join(ind,how="outer")
print(datafeed)
################
################
################

# get and add data feed 
data = custemData(dataname=datafeed)
cerebro.adddata(data)

cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

#cerebro.plot(iplot=False)