import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.coins = {}

        for coin in self.datas:
            self.coins[coin._name] = coin

    def next(self):
        pass
        # Simply log the closing price of the series from the reference

        a = self.coins["SOL"].get(size=3, ago=-3)
        self.log(f"{a}")
        
        # self.log(f"{self.coins['SOL'][0]}")

