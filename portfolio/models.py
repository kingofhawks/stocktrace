from django.db import models
from django.utils import timezone
from django.conf import settings

db = settings.DB


# Create your models here.
class Portfolio(object):
    #static variable here
    position_ratio_limit = 90

    def __init__(self, stocks):
        self.stocks = stocks
        self.market_value = 0
        self.total = 0
        for stock in self.stocks:
            try:
                if stock['code'] == '999999':
                    print 'cash:{}'.format(stock['amount'])
                else:
                    self.market_value += float(stock['amount'])*float(stock['current'])
                self.total += float(stock['amount'])*float(stock['current'])
            except KeyError as e:
                pass
        self.position_ratio = self.market_value/self.total
        self.date = timezone.now()

    def save(self):
        stock_list = []
        for stock in self.stocks:
            stock_list.append({'code': stock['code'], 'amount': stock['amount'], 'current': stock['current']})
        db.portfolio.insert({'date': self.date, 'stocks': stock_list, 'market_value': self.market_value,
                             'total': self.total, 'position_ratio': self.position_ratio})
