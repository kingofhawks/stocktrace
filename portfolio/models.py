#-*- coding: UTF-8 -*-
from django.conf import settings
from mongoengine import Document, ListField, FloatField, DateTimeField

db = settings.DB


def get_stocks():
    # stocks = [{'code': '600420', 'amount': 10000 + 7800 + 6200}, {'code': '600177', 'amount': 20000 + 2000},
    #           {'code': '000028', 'amount': 2000 + 500}, {'code': '300246', 'amount': 2200 + 2000 + 3300},
    #           {'code': '601997', 'amount': 1000 + 3500 + 3000},
    #           {'code': '601818', 'amount': 20000}, {'code': '601009', 'amount': 4000 + 3000},
    #           {'code': '600995', 'amount': 3000 + 2700}, {'code': '002589', 'amount': 500 + 2300},
    #           {'code': '601688', 'amount': 1000 + 2000}, {'code': '002468', 'amount': 600 + 900},
    #           {'code': '600383', 'amount': 1800},
    #           {'code': '510900', 'amount': 20000},
    #           {'code': '600533', 'amount': 2000 + 2800},
    #           {'code': '601933', 'amount': 1400}, {'code': '510500', 'amount': 3000 + 1000},
    #           {'code': '510050', 'amount': 2000},
    #           {'code': '131810', 'amount': 12900 + 2800},]
    stock = db.stock
    stocks = stock.find({"amount": {"$gt": 0}})
    print(stocks)
    return stocks


class Portfolio(Document):
    # static variable here
    position_ratio_limit = 90
    date = DateTimeField()
    list = ListField(dict())
    # 市值
    market_value = FloatField()
    # 总资产
    total = FloatField()
    net_asset = FloatField()
    cost = FloatField()
    cost_history = FloatField()
    # ZS账户当年(真实)本金
    cost_zs = FloatField(default=463000+4000)
    # 券商融资+江苏银行
    financing = FloatField(default=169366 + 70000)
    cost_ht1 = FloatField()
    cost_ht2 = FloatField()
    cost_ht1_real = FloatField()
    cost_ht2_real = FloatField()
    position_ratio = FloatField()
    lever = FloatField()
    cash = FloatField()
    profit = FloatField()
    profit_ratio = FloatField()
    profit_today = FloatField()
    profit_ratio_today = FloatField()

    def compute(self):
        # HT1账户当年本金
        self.cost_ht1 = 277461+17000+5000
        # HT1账户真实本金
        self.cost_ht1_real = 226000+17000+5000
        # HT2账户当年本金
        self.cost_ht2 = 218579+20000
        # HT2账户真实本金
        self.cost_ht2_real = 210000+20000
        # 三个账户当年本金
        self.cost = self.cost_zs+self.cost_ht1+self.cost_ht2
        # 三个账户真实本金
        self.cost_history = self.cost_zs+self.cost_ht1_real+self.cost_ht2_real

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

        for stock in self.list:
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
        print('total:{}'.format(self.total))
        # 仓位
        self.position_ratio = 0
        # 杠杆
        self.lever = 0

        if self.total != 0:
            self.position_ratio = float("{0:.2f}".format(self.market_value*100/self.total))
            self.lever = float("{0:.2f}".format(self.total*100/self.net_asset))
            # 个股占比
            for stock in self.list:
                try:
                    if stock['code'] == '131810':
                        value = float(stock['amount'])*100/self.total
                        stock['ratio'] = float("{0:.2f}".format(value))
                        stock['market'] = float(stock['amount'])
                    else:
                        value = float(stock['amount']) * float(stock['current'])
                        stock['ratio'] = float("{0:.2f}".format(value*100 / self.total))
                        stock['market'] = float("{0:.2f}".format(value))
                except KeyError as e:
                    pass
        print('stocks:{}'.format(self.list))
        self.profit = self.net_asset - self.cost
        # 以成本入账
        self.profit_ratio = float("{0:.2f}".format(self.profit*100/self.cost))
        # 以净资产入账
        self.profit_ratio_today = float("{0:.2f}".format(self.profit_today*100/self.net_asset))

    def __unicode__(self):
        return self.date
