import backtrader as bt
from btFunc import *

cerebro = bt.Cerebro(runonce=False)
cerebro.broker.setcash(100000000.0)
#cerebro.addstrategy(TestStrategy)