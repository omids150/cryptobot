import backtrader as bt
import lagtestV2 as lg 

############ GET CORR DATA #############
def get_corr_data(start=30):
    main_coin_dict = lg.get_main_coins_eod(start=start)
    coins = lg.joinTimeSeries(main_coin_dict)
    coins = coins.drop(columns=["BTC","ETH","ADA","XRP","SOL","scaled_price","returns","scaled_price_std"])
    return coins

########## DEF FEED #################################
class custemData(bt.feeds.PandasData):
    lines = ("rolling",)
    params = (("rolling", 8),)
    pass

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].rolling

    def next(self):
        # pass
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])