import backtrader as bt
import lagtestV2 as lg 

############ GET CORR DATA #############
def get_corr_data(start=30):
    main_coin_dict = lg.get_main_coins_eod(start=start)
    coins = lg.joinTimeSeries(main_coin_dict,window=700)
    coins = coins.drop(columns=["BTC","ETH","ADA","XRP","SOL","scaled_price","returns"])
    #"scaled_price_std"
    return coins

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.close = self.datas[0]

    # def nextstart(self):
    #     # Buy all the available cash
    #     self.buy(size=10) 

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log(f"{self.close[0]}")
        a = self.close.get(size=6)
        self.log(f"{a}")
        