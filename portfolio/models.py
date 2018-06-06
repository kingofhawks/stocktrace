#-*- coding: UTF-8 -*-
from django.db import models
from django.utils import timezone
from datetime import datetime, date
from django.conf import settings
from mongoengine import Document

db = settings.DB


class Portfolio(Document):
    # static variable here
    position_ratio_limit = 90

    def __init__(self, stocks, name=None):
        if name:
            self.name = name
        else:
            self.name = str(date.today())
        self.stocks = stocks
        # 三个账户真实本金
        self.cost_history = 493000+210000+226000
        # ZS账户当年本金
        self.cost_zs = 463000
        # HT1账户当年本金
        self.cost_ht1 = 277461
        # HT2账户当年本金
        self.cost_ht2 = 218579
        # 三个账户当年本金
        self.cost = self.cost_zs+self.cost_ht1+self.cost_ht2
        # 券商融资+江苏银行
        self.financing = 156765+30000
        # 市值
        self.market_value = 0
        # 总资产
        self.total = 0
        # 现金
        self.cash = 0
        # 净资产
        self.net_asset = 0
        # 盈利
        self.profit = 0
        # 盈利率
        self.profit_ratio = 0
        # 当日盈利
        self.profit_today = 0
        # 当日盈利%
        self.profit_ratio_today = 0

        for stock in self.stocks:
            try:
                if stock['code'] == '131810':
                    self.cash += float(stock['amount'])
                else:
                    value = float(stock['amount'])*float(stock['current'])
                    self.market_value += value
                    self.profit_today += float(stock['amount'])*float(stock['change'])
            except KeyError as e:
                pass
        self.total += self.market_value+self.cash
        self.net_asset = self.total - self.financing

        # 仓位
        self.position_ratio = 0
        # 杠杆
        self.lever = 0
       
        if self.total != 0:
            self.position_ratio = float("{0:.2f}".format(self.market_value*100/self.total))
            self.lever = float("{0:.2f}".format(self.total*100/self.net_asset))
            # 个股占比
            for stock in self.stocks:
                try:
                    if stock['code'] == '131810':
                        value = float(stock['amount'])*100/self.total
                        stock['ratio'] = float("{0:.2f}".format(value))
                        stock['market'] = float(stock['amount'])
                    else:
                        value = float(stock['amount']) * float(stock['current'])
                        stock['ratio'] = float("{0:.2f}".format(value*100 / self.total))
                        stock['market'] = value
                except KeyError as e:
                    pass
        self.profit = self.net_asset - self.cost
        # 以成本入账
        self.profit_ratio = float("{0:.2f}".format(self.profit*100/self.cost))
        # 以净资产入账
        self.profit_ratio_today = float("{0:.2f}".format(self.profit_today*100/self.net_asset))
        self.date = datetime.now()

    def save(self):
        stock_list = []
        for stock in self.stocks:
            stock_list.append({'code': stock['code'], 'amount': stock['amount'], 'current': stock['current']})
        db.portfolio.insert({'name': self.name, 'date': self.date, 'stocks': stock_list,
                             'market_value': self.market_value,
                             'total': self.total, 'net_asset': self.net_asset, 'financing': self.financing,
                             'position_ratio': self.position_ratio, 'lever': self.lever,
                             'profit': self.profit, 'profit_ratio': self.profit_ratio,
                             'profit_today': self.profit_today, 'profit_ratio_today': self.profit_ratio_today})

    def __unicode__(self):
        return self.name
