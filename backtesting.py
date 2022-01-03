import backtrader as bt
import lagtestV2 as lg 
import pandas as pd

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000.0)

# get and add data feed 
dataframe = lg.get_coin_by_name_eod("BTC")
print(dataframe.head())
dataframe = dataframe.drop(columns=['gmtoffset', 'scaled_price'])

dataframe.index = pd.to_datetime(dataframe.index)

print(type(dataframe.index))


data = bt.feeds.PandasData(dataname=dataframe)
cerebro.adddata(data)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

