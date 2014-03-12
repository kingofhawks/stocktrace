#from datetime import date
from stocktrace.util import slf4p, settings




logger = slf4p.getLogger(__name__)


class Stock:
    mgsy = 0 #EPS TTM
    mgjzc = 0 #booking value MRQ
    pe = 0;#dynamic PE
    lastYearPe = 0#last year static PE
    pb = 0;
    ps = 0;#price/sales ratio
    rank = 0;
    lastUpdate = '';
    totalCap = 0;
    floatingCap = 0;
    date = '';
    close = 0;
    openPrice = 0;
    volume = 0;
    hasGap = False;
    name = '';
    yearHigh = 0;
    yearLow = 0;
    PercentChangeFromYearLow = 0;
    PercentChangeFromYearHigh = 0;
    ma50 = 0;
    ma200 = 0;
    PercentChangeFromTwoHundreddayMovingAverage = '';
    PercentChangeFromFiftydayMovingAverage = '';
    alert = False;
    state = 'OK'#OK,WARNING,CRITICAL,UP
    isInSh = False;#Shanghai code

    def __init__(self, code, current=0, percent=0, low=0, high=0, volume=0):
        self.code = code
        self.current = current
        self.percent = percent
        self.low = low
        self.high = high
        self.volume = volume

    def __str__(self):
        #self.pe = self.current/self.mgsy
        return self.code + '**name:' + str(self.name) + '**now:' + str(
            self.current) + '**state:' + self.state + '**percent:' + str('%.2f' % self.percent + '%') + '**high:' + str(
            '%.2f' % self.high) + '**low:' + str('%.2f' % self.low) + '**alarm:' + str(self.alert) + '**open:' + str(
            '%.2f' % self.openPrice) + '**close:' + str('%.2f' % self.close) + '**volume:' + str(
            self.volume) + '**PE:' + str('%.2f' % self.pe) + '**PB:' + str('%.2f' % self.pb) + '**rank:' + str(
            '%.2f' % self.rank) + '**EPS:' + str(self.mgsy) + '**mgjzc:' + str(self.mgjzc) + '**last:' + str(
            self.lastUpdate) + '**totalCap:' + str('%.2f' % (self.totalCap / 10000)) + '**marketCap:' + str(
            '%.2f' % (self.floatingCap / 10000)) + '**date:' + str(self.date)

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


def download_stock(stock, download_latest=True, realtime_engine=settings.SINA, download_history=True,
             history_engine=settings.CSV_ENGINE, download_statistics=False):
    logger.info('Start download finance data:{}'.format(stock.code))

    #download statistics from reuters
    if download_statistics:
        from stocktrace.parse.reutersparser import downloadKeyStatDatas
        downloadKeyStatDatas()

    #update latest price from yahoo or sina
    #Seems YQL API is not stable,tables often to be locked
    if download_latest:
        from stocktrace.parse.sinaparser import update
        update(stock.code,realtime_engine)

    if download_history:
    #    #download history data from yahoo CSV or YDN
        from stocktrace.parse.yahooparser import download_history_data
        download_history_data(stock.code, save=True, begin_date='2012-01-01')

    logger.info('Finish download finance data:{}'.format(stock.code))


