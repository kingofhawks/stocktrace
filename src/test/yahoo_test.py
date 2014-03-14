import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace.parse.yahooparser import download_history_data
from stocktrace.dao.stockdao import findAllQuotes,findStockByCode,find_week52_history,update_week52,remove_stock
from stocktrace.util import slf4p,settings
from stocktrace.parse.sinaparser import update
from stocktrace.stock import Stock,download_stock

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600583'
    sh = Stock('600327')
    sz = Stock('000563')
    # 601318

    def test_print_stock(self):
        print self.sh

    def test_remove_stock(self):
        remove_stock(self.sh.code)

    def test_download_sh(self):
        download_stock(self.sh,download_latest=True, realtime_engine=settings.SINA, download_history=True,
             history_engine=settings.CSV_ENGINE, download_statistics=False)

    def test_download_sz(self):
        download_stock(self.sz,download_latest=True, realtime_engine=settings.YAHOO, download_history=True,
             history_engine=settings.YAHOO, download_statistics=False)

    def test_sina_latest(self):
        update(self.code,engine='sina')

    def test_ydn_latest(self):
        update(self.code,engine='yahoo')

    def test_re_download(self):
        from stocktrace.data.download import download2
        from stocktrace.util import settings
        download2(clearAll= True,downloadLatest = True,downloadHistory = True,parse_industry = False,stockList=settings.STOCK_LIST_HOLD);

    def test_download(self):
        from stocktrace.data.download import download
        from stocktrace.util import settings
        download(clearAll= True,downloadLatest = True,downloadHistory = True,parse_industry = False,stockList=settings.STOCK_LIST_HOLD);


    def test_download2(self):
        from stocktrace.data.download import download
        from stocktrace.util import settings
        download(clearAll= True,downloadLatest = True,downloadHistory = True,parse_industry = False,stockList=settings.STOCK_LIST_TOP100);





    def test_poll_ydn(self):
        download_history_data(self.code,True,engine = 'ydn')

    def test_yahoo_csv(self):
        download_history_data(self.code,True)

    def test_yahoo_csv2(self):
        url = 'http://ichart.finance.yahoo.com/table.csv?s=601318.SS&d=2&e=08&f=2014&a=0&b=01&c=2012'
        import requests
        r = requests.get(url)
        r.status_code
        logger.debug(r.text)
        # downloadHistorialData(self.code,True)

    def test_week52(self):
        history = find_week52_history(self.code)
        logger.debug(history)
        logger.debug(history.count())
        # for h in history:
        #     logger.debug(h)

    def test_update_week52(self):
        update_week52(self.code)


    def test_yahoo(self):
        update(self.code,engine='sina')


    def test_pandas(self):
        import pandas as pd
        # result = findStockByCode('600327')
        result = find_week52_history(self.code)
        logger.debug(result)
        df = pd.DataFrame(list(result))
        logger.debug(df)
        logger.debug(df.shape)
        logger.debug(df['low'].min())
        logger.debug(df['low'].argmin())
        logger.debug(df['high'].max())
        high_week52_index = df['high'].argmax()
        low_week52_index = df['low'].argmin()
        logger.debug(high_week52_index)
        logger.debug(df[['date','high']][high_week52_index:high_week52_index+1])
        logger.debug(df[['date','low']][low_week52_index:low_week52_index+1])
