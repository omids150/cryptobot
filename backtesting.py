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

# class tPandasData(bt.feed.DataBase):
#     '''
#     The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
#     DataFrame
#     '''

#     params = (
#         # Possible values for datetime (must always be present)
#         #  None : datetime is the "index" in the Pandas Dataframe
#         #  -1 : autodetect position or case-wise equal name
#         #  >= 0 : numeric index to the colum in the pandas dataframe
#         #  string : column name (as index) in the pandas dataframe
#         ('datetime', None),

#         # Possible values below:
#         #  None : column not present
#         #  -1 : autodetect position or case-wise equal name
#         #  >= 0 : numeric index to the colum in the pandas dataframe
#         #  string : column name (as index) in the pandas dataframe
#         ('open', -1),
#         ('high', -1),
#         ('low', -1),
#         ('close', -1),
#         ('volume', -1),
#         ('openinterest', -1),
#     )


dataframe2 = get_scaled_price()
data2 = bt.feeds.PandasData(dataname=dataframe2)
print(dataframe)
cerebro.adddata(data2)

cerebro.broker.setcommission(commission=0.001)


print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run(unonce=False)

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot(iplot=False)