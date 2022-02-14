import backtrader as bt
import lagtestV2 as lg 

############ GET CORR DATA #############
def get_corr_data(start=30):
    main_coin_dict = lg.get_main_coins_eod(start=start)
    coins = lg.joinTimeSeries(main_coin_dict,window=700)
    coins = coins.drop(columns=["BTC","ETH","ADA","XRP","SOL","scaled_price","returns"])
    #"scaled_price_std"
    return coins

########## DEF FEED #################################
class custemData(bt.feeds.PandasData):
    lines = ("rolling","scaled_price","scaled_price_std")
    params =(
            ("scaled_price",5),
            ("scaled_price_std",6),
            ("rolling", 7),
            )
    
# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.rolling = self.datas[0].rolling
        self.scaled_price = self.datas[0].scaled_price
        self.scaled_price_std = self.datas[0].scaled_price_std[0]        
    
    def nextstart(self):
        # Buy all the available cash
        self.buy(size=10) 

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log(f'scaled price: {self.scaled_price[0]} rolling: {self.rolling[0]} std_scaled_price: {self.scaled_price_std}')

        last_action_sell = None

        if self.scaled_price < self.scaled_price_std-self.rolling:
            self.order = self.buy()
        elif self.scaled_price > self.scaled_price_std+self.rolling:
            self.order = self.sell()
        