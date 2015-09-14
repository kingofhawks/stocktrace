from django.db import models


# Create your models here.
class Market(object):
    '''
    classdocs
    '''

    def __init__(self, name, total_market_cap, volume, turnover_rate, pe):
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
        return '{} total market:{} volume:{} turnover rate:{} PE:{}'.format(self.name, self.total_market_cap,
                                                                         self.volume, self.turnover_rate, self.pe)
