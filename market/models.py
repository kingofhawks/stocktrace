from django.db import models


# Create your models here.
class Market(object):
    '''
    classdocs
    '''
    # ssgs = 0
    # sszq = 0
    # ssgp = 0
    # totalShares = 0
    # totalFloatingShares = 0
    # totalCap = 0
    # totalMarketCap = 0
    # marketPe = 0
    # avgPrice = 0

    def __init__(self, total_market_cap, volume, turnover_rate, pe):
        try:
            self.total_market_cap = float(total_market_cap)
        except TypeError:
            self.total_market_cap = 0

        try:
            self.volume = float(volume)
        except TypeError:
            self.volume = 0

        try:
            self.turnover_rate = float(turnover_rate)
        except TypeError:
            self.turnover_rate = 0

        try:
            self.pe = float(pe)
        except TypeError:
            self.pe = 0

        '''
        Constructor
        '''

    def __str__(self):
        return 'total market:{} volume:{} turnover rate:{} PE:{}'.format(self.total_market_cap,
                                                                         self.volume, self.turnover_rate, self.pe)
