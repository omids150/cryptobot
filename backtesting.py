import backtrader as bt
import lagtestV2 as lg 

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000.0)

# get and add data feed 
dataframe = lg.get_coin_by_name_eod("BTC")

dataframe = dataframe.drop(columns=['gmtoffset', 'scaled_price'])
print(dataframe.dtypes)

data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

