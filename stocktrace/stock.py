#-*- coding: UTF-8 -*-
#from datetime import date
from mongoengine import *


class Stock(Document):
    code = StringField()
    name = StringField()
    current = FloatField()
    percentage = FloatField()
    volume = FloatField()
    open_price = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    low52week = FloatField()
    high52week = FloatField()
    # NH-NL index
    nh = BooleanField(default=False)
    nl = BooleanField(default=False)
    pb = FloatField()
    # EPS TTM
    mgsy = FloatField()
    # booking value MRQ
    mgjzc = FloatField()
    # PE TTM
    pe_ttm = FloatField()
    # last year static PE
    pe_lyr = FloatField()
    # PS ratio
    ps = FloatField()
    rank = FloatField()
    lastUpdate = DateTimeField()
    totalCap = FloatField()
    floatingCap = FloatField()
    date = DateTimeField()
    hasGap = BooleanField(default=False)
    PercentChangeFromYearLow = FloatField()
    PercentChangeFromYearHigh = FloatField()
    ma50 = FloatField()
    ma200 = FloatField()
    PercentChangeFromTwoHundreddayMovingAverage = FloatField()
    PercentChangeFromFiftydayMovingAverage = FloatField()
    alert = BooleanField(default=False)
    state = StringField(default='OK')  # OK,WARNING,CRITICAL,UP
    isInSh = BooleanField(default=False)  # Shanghai code
    amount = IntField(default=0)
    tags = ListField(StringField())
    up_threshold = FloatField()
    down_threshold = FloatField()

    def __init__(self, *args, **kwargs):
            Document.__init__(self, *args, **kwargs)

            if self.low52week != 0 and self.close:
                self.PercentChangeFromYearLow = (float(self.close) - float(self.low52week))/float(self.low52week)

            if self.high52week != 0 and self.close:
                self.PercentChangeFromYearHigh = (float(self.close) - float(self.high52week))/float(self.high52week)

            if self.low52week != 0 and self.low52week == self.low:
                self.nl = True

            if self.high52week != 0 and self.high52week == self.high:
                self.nh = True

    #python2.7 use __unicode__, for python3 use __str__
    def __unicode__(self):
        return self.code + '**name:' + str(self.name) + '**now:' + str(
            self.current) + '**state:' + self.state + '**percent:' + str('%.2f' % self.percent + '%') + '**high:' + str(
            '%.2f' % self.high) + '**low:' + str('%.2f' % self.low) + '**alarm:' + str(self.alert) + '**open:' + str(
            '%.2f' % self.openPrice) + '**close:' + str('%.2f' % self.close) + '**volume:' + str(
            self.volume) + '**PE:' + str('%.2f' % self.pe) + '**PB:' + str('%.2f' % self.pb) + '**rank:' + str(
            '%.2f' % self.rank) + '**EPS:' + str(self.mgsy) + '**mgjzc:' + str(self.mgjzc) + '**last:' + str(
            self.lastUpdate) + '**totalCap:' + str('%.2f' % (self.totalCap / 10000)) + '**marketCap:' + str(
            '%.2f' % (self.floatingCap / 10000)) + '**date:' + str(self.date)

    def __str__(self):
        return 'code:{} name:{} current:{} percentage:{} open:{} high:{} low:{} close:{} ' \
               'low52week:{} nl:{}  high52week:{} nh:{} PercentChangeFromYearLow:{} PercentChangeFromYearHigh:{} ' \
               'pe:{} pb:{} date:{}'.format(
            self.code, self.name, self.current, self.percentage, self.open_price, self.high, self.low, self.close,
            self.low52week, self.nl, self.high52week, self.nh,  self.PercentChangeFromYearLow, self.PercentChangeFromYearHigh,
            self.pe_lyr, self.pb, self.date
        )

    def shortStr(self):
        return self.code + str('|%.2f' % self.percent + '%') + '|state:' + self.state + '|now:' + str(
            self.current) + '|high:' + str('%.2f' % self.high) + '|low:' + str('%.2f' % self.low) + '|volume:' + str(
            '%.2f' % (self.volume / 100)) + '|alarm:' + str(self.alert)

    def yearHighLow(self):
        return self.code + str('|%.2f' % self.percent + '%') + '|now:' + str(self.current) + '|yearHigh:' + str(
            '%.2f' % self.yearHigh) + '|yearLow:' + str('%.2f' % self.yearLow) + '|PercentChangeFromYearHigh:' + str(
            '%.2f' % (self.PercentChangeFromYearHigh)) + '|PercentChangeFromYearLow:' + str(
            self.PercentChangeFromYearLow)

    def compute(self):
        if (self.lastUpdate.find('03-31') != -1):
            self.pe = self.current / (float(self.mgsy) * 4)
        elif (self.lastUpdate.find('06-30') != -1):
            self.pe = self.current / (float(self.mgsy) * 4 / 2)
        elif (self.lastUpdate.find('09-30') != -1):
            self.pe = self.current / (float(self.mgsy) * 4 / 3)
        elif (self.lastUpdate.find('12-31')!= -1):
            self.pe = self.current/float(self.mgsy)
        if (self.mgjzc!= 0):
            self.pb = self.current/float(self.mgjzc)
        self.rank = self.pe * self.pb

    def download_stock(self, download_latest=True, realtime_engine='sina', download_history=True,
                       history_engine='csv', download_statistics=False):
        # logger.info('Start download finance data:{}'.format(stock.code))

        #download statistics from reuters
        if download_statistics:
            from stocktrace.parse.reutersparser import downloadKeyStatDatas
            downloadKeyStatDatas()

        #update latest price from yahoo or sina
        #Seems YQL API is not stable,tables often to be locked
        if download_latest:
            from stocktrace.parse.sinaparser import update
            update(self.code, realtime_engine)

        if download_history:
        #    #download history data from yahoo CSV or YDN
            from stocktrace.parse.yahooparser import download_history_data
            download_history_data(self.code, save=True, begin_date='2012-01-01')

        if realtime_engine == 'sina' and history_engine == 'csv':
            from stocktrace.dao.stockdao import update_week52
            update_week52(self.code)

        # logger.info('Finish download finance data:{}'.format(stock.code))


class StockHistory(Document):
    code = StringField()
    percent = FloatField()
    volume = FloatField()
    open_price = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    pb = FloatField()
    time = DateTimeField()
    timestamp = IntField()
    turn_rate = FloatField()
    ma5 = FloatField()
    ma10 = FloatField()
    ma30 = FloatField()

    def __str__(self):
        return 'code:{} percent:{} open:{} high:{} low:{} close:{} turnover:{} time:{}' .format(self.code,
               self.percent, self.open_price, self.high, self.low, self.close, self.turn_rate, self.time
        )



