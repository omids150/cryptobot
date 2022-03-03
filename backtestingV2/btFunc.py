import backtrader as bt
import numpy as np

window = 1

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.coins = {}

        for coin in self.datas: self.coins[coin._name] = coin


    def next(self):
        # Simply log the closing price of the series from the reference

        avg = np.array([])
        for coin in self.coins.items():
            c = coin[1].get(size=window)
            
            c += c

            self.log(c)

            avg += c
            self.log(f"{avg}")

        else: 
            self.log(f"-----------------------")
