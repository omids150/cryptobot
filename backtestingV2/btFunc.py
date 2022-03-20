import backtrader as bt
import numpy as np

window = 2

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

        avg_array = [0 for i in range(0,2)]
        avg_array = np.array(avg_array)

        self.log(f"{avg_array}")

        for coin in self.coins.items():
            c = coin[1].get(size=window)
            
            #c = np.array(c)
            
            self.log(c[-1])
            #self.log(type(c[1]))

            #avg_array += c

            #self.log(avg_array[0])

        else: 
            self.log(f"-----------------------")
