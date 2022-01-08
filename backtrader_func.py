import backtrader as bt
from numpy.testing._private.utils import print_assert_equal

import lagtestV2 as lg 

class MyInd(bt.Indicator):
    lines = ('ind',)

    def __init__(self):
        main_coins = lg.get_main_coins_eod()
        join = lg.joinTimeSeries(main_coins)

        join = join.drop(columns = ["BTC","ETH","ADA","XRP","SOL","returns","rolling","scaled_price_std"])

        print(join)
        data = bt.feeds.PandasData(dataname=join)

        self.lines.ind = data

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.myInd = MyInd()

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        
        # self.log(self.myInd)