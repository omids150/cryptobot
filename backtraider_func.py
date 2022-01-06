import backtrader as bt
from numpy.core.fromnumeric import amin

import lagtestV2 as lg 

class OverUnderMovAv(bt.Indicator):
    lines = ('overunder',)
    # params = dict(period=20, movav=bt.ind.MovAv.Simple)

    # plotinfo = dict(
    #     # Add extra margins above and below the 1s and -1s
    #     plotymargin=0.15,

    #     # Plot a reference horizontal line at 1.0 and -1.0
    #     plothlines=[1.0, -1.0],

    #     # Simplify the y scale to 1.0 and -1.0
    #     plotyticks=[1.0, -1.0])

    # # Plot the line "overunder" (the only one) with dash style
    # # ls stands for linestyle and is directly passed to matplotlib
    # plotlines = dict(overunder=dict(ls='--'))

    # def _plotlabel(self):
    #     # This method returns a list of labels that will be displayed
    #     # behind the name of the indicator on the plot

    #     # The period must always be there
    #     plabels = [self.p.period]

    #     # Put only the moving average if it's not the default one
    #     plabels += [self.p.movav] * self.p.notdefault('movav')

    #     return plabels

    def __init__(self):
        main_coins = lg.get_main_coins_eod()
        ind = lg.joinTimeSeries(main_coins)
        self.l.overunder = list(ind["scaled_price"])

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.test = OverUnderMovAv()

    def next(self):
        # Simply log the closing price of the series from the reference
        #self.log('Close, %.2f' % self.dataclose[0])
        self.log(self.test)
