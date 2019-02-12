#-*- coding: UTF-8 -*-
from django.conf import settings
from mongoengine import Document, ListField, FloatField, DateTimeField, StringField

db = settings.DB


@DeprecationWarning
def get_stocks():
    stock = db.stock
    stocks = stock.find({"amount": {"$gt": 0}})
    print(stocks)
    return stocks


def get_stocks_from_latest_portfolio():
    latest_portfolio = Portfolio.objects().order_by('-date').first()
    date = latest_portfolio.date
    portfolio = Portfolio.objects(date=date).first()
    stocks = portfolio.list
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
    # 期权账户本金
    cost_option = FloatField(default=7000+3000+5000+5000+10000)
    # ZS账户当年(真实)本金
    cost_zs = FloatField(default=463000+4000+10000+15000+8000)
    # 融资利息江苏银行(2018年7月至2019年1月1日)
    js_interest = FloatField(default=2600+735+830)
    # 券商融资+江苏银行
    financing = FloatField(default=170710 + 160000)
    # HT1账户当年资金变动(老婆)
    ht1_changes = 17000 + 5000 + 5000 + 20000 + 20000
    # HT2账户当年资金变动(老妈)
    ht2_changes = 20000
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
        self.cost_ht1 = 277461+self.ht1_changes
        # HT1账户真实本金
        self.cost_ht1_real = 226000+self.ht1_changes
        # HT2账户当年本金
        self.cost_ht2 = 218579+self.ht2_changes
        # HT2账户真实本金
        self.cost_ht2_real = 210000+self.ht2_changes
        # 四个账户当年本金
        self.cost = self.cost_zs+self.cost_ht1+self.cost_ht2+self.cost_option+self.js_interest
        # 四个账户真实本金
        self.cost_history = self.cost_zs+self.cost_ht1_real+self.cost_ht2_real+self.cost_option+self.js_interest

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
            print('code:{}'.format(stock['code']))

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
        self.profit = float("{0:.2f}".format(self.net_asset - self.cost))
        # 以成本入账
        self.profit_ratio = float("{0:.2f}".format(self.profit*100/self.cost))
        # 以净资产入账
        self.profit_ratio_today = float("{0:.2f}".format(self.profit_today*100/self.net_asset))

    def __unicode__(self):
        return self.date


# 分红
class Dividend(Document):
    money = FloatField()
    date = DateTimeField()
    description = StringField()
