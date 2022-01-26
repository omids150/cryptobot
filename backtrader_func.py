import backtrader as bt

import lagtestV2 as lg 


def get_scaled_price():
    main_coins = lg.get_main_coins_eod()
    join = lg.joinTimeSeries(main_coins)

    #join = join.drop(columns = ["BTC","ETH","ADA","XRP","SOL","returns","rolling","scaled_price_std"]) #scaled_price
    join = join.drop(columns = ["ETH","ADA","XRP","SOL","returns","rolling","scaled_price_std"]) #scaled_price

    return join


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        #self.scale = self.datas[0].scaled_data
    def next(self):
        # Simply log the closing price of the series from the reference
        pass
        #self.log('Close, %.2f' % self.scale )
        