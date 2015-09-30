#-*- coding: UTF-8 -*-
from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.conf import settings

db = settings.DB


class Portfolio(object):
    #static variable here
    position_ratio_limit = 90

    def __init__(self, stocks, name=None):
        if name:
            self.name = name
        else:
            self.name = str(date.today())
        self.stocks = stocks
        self.market_value = 0
        self.total = 0
        #融资
        self.financing = 0
        for stock in self.stocks:
            try:
                if stock['code'] == '999999':
                    print 'cash:{}'.format(stock['amount'])
                elif stock['code'] == '999998':
                    self.financing = float(stock['amount'])
                else:
                    self.market_value += float(stock['amount'])*float(stock['current'])
                self.total += float(stock['amount'])*float(stock['current'])
            except KeyError as e:
                pass
        # from decimal import *
        # getcontext().prec = 2
        # self.position_ratio = Decimal(self.market_value)/Decimal(self.total)
        self.position_ratio = 0
        if self.total != 0:
            self.position_ratio = self.market_value/self.total
        # self.date = timezone.now()
        self.date = datetime.now()

    def save(self):
        stock_list = []
        for stock in self.stocks:
            stock_list.append({'code': stock['code'], 'amount': stock['amount'], 'current': stock['current']})
        db.portfolio.insert({'name':self.name, 'date': self.date, 'stocks': stock_list,
                             'market_value': self.market_value,
                             'total': self.total, 'position_ratio': self.position_ratio})

    def __unicode__(self):
        return self.name
