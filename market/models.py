from django.db import models


# Create your models here.
class Market(object):
    '''
    classdocs
    '''

    def __init__(self, name, total_market_cap, volume, turnover, pe):
        self.name = name
        try:
            self.total_market_cap = float(total_market_cap)
        except TypeError:
            self.total_market_cap = 0

        try:
            self.volume = float(volume)
        except TypeError:
            self.volume = 0

        try:
            self.turnover = float(turnover)
        except TypeError:
            self.turnover = 0

        try:
            self.pe = float(pe)
        except TypeError:
            self.pe = 0

        '''
        Constructor
        '''

    def __str__(self):
        return '{} total market:{} volume:{} turnover rate:{} PE:{}'.format(self.name, self.total_market_cap,
                                                                         self.volume, self.turnover, self.pe)
