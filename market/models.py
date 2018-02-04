from django.db import models
from mongoengine import *
import datetime


# Create your models here.
class Index(Document):
    name = StringField()
    # 静态PE
    pe = FloatField()
    # 滚动
    pe_ttm = FloatField()
    pb = FloatField()
    # 股息率
    dividend_yield_ratio = FloatField()
    total_market_cap = FloatField()
    volume = FloatField()
    turnover = FloatField()
    value = FloatField()
    date = DateTimeField()

    def __str__(self):
        return 'index:{} PE:{} PE_TTM:{} PB:{} DYR:{} Date:{}'.format(self.name,
                self.pe, self.pe_ttm, self.pb, self.dividend_yield_ratio, self.date)


class AhIndex(Document):
    value = FloatField()
    date = DateTimeField(default=datetime.datetime.now())


class Sw(Document):
    # BargainDate = DateTimeField()
    # !use IntField instead of DateTimeField, highcharts will render x-axis time series data with timestamp value
    BargainDate = IntField()
    PB = FloatField()
    PE = FloatField()
    TurnoverRate = FloatField()
    SwIndexName = StringField()
    CloseIndex = FloatField()
    MeanPrice = FloatField()
    BargainSumRate = FloatField()
    SwIndexCode = StringField()
    BargainAmount = IntField()
    Markup = FloatField()
    DP = FloatField()


class Cix(Document):
    value = FloatField()
    timestamp = IntField()
    pe = FloatField()
    low_pb = FloatField()
    ah = FloatField()
    high_price = FloatField()