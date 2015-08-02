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
        self.total_market_cap = total_market_cap
        self.volume = volume
        self.turnover_rate = turnover_rate
        self.pe = pe
        '''
        Constructor
        '''

    def __str__(self):
        return 'total market:{} volume:{} turnover rate:{} PE:{}'.format(self.total_market_cap,
                                                                         self.volume, self.turnover_rate, self.pe)
