import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace.parse.yahooparser import download_history_data
from stocktrace.dao.stockdao import findPeakStockByDays,findStockByCode,find_week52_history,update_week52,remove_stock,find_percentage,findAllExistentTickers
from stocktrace.util import slf4p,settings
from stocktrace.parse.sinaparser import update
from stocktrace.stock import Stock,download_stock
from stocktrace.data.download import download2
from stocktrace.parse.screener import findByNhnl
from datetime import date
from datetime import timedelta
from datetime import datetime

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600583'
    sh = Stock('600327')
    sz = Stock('002236')
    # 601318

    def test_peak_price(self):
        logger.debug(findPeakStockByDays('000776',50))

    def test_peak_price(self):
        delta = timedelta(-20)
        begin = date.today()+delta
        #begin_date ='2014-1-1'
        #rise('600327',begin)
        # find_percentage(['600327','600583'],'2014-01-01')
        result = find_percentage(findAllExistentTickers(),'2014-01-01')
        for stock in result:
            logger.debug(stock.shortStr())

