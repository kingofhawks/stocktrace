from django.db import models
from django.utils import timezone
from django.conf import settings

#print settings
#print settings.CACHES
#print settings.DB
db = settings.DB

# Create your models here.
class Portfolio(object):

    def __init__(self, stocks):
        self.stocks = stocks
        self.market_value = 0
        for stock in self.stocks:
            try:
                self.market_value += float(stock['amount'])*float(stock['current'])
            except KeyError as e:
                pass
        self.date = timezone.now()

    def save(self):
        #client = MongoClient('localhost', 27017)
        #cache = Cache()
        #db = client.stocktrace
        stock_list = []
        for stock in self.stocks:
            stock_list.append({'code': stock['code'], 'amount': stock['amount'], 'current': stock['current']})
        db.portfolio.insert({'date': self.date, 'stocks': stock_list, 'market_value': self.market_value})
