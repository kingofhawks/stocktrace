import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace.parse.yahooparser import download_history_data
from stocktrace.dao.stockdao import findPeakStockByDays,findStockByCode,find_week52_history,update_week52,remove_stock
from stocktrace.util import slf4p,settings
from stocktrace.parse.sinaparser import update
from stocktrace.stock import Stock,download_stock
from stocktrace.data.download import download2
from stocktrace.parse.screener import findByNhnl

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600583'
    sh = Stock('600327')
    sz = Stock('002236')
    # 601318

    def test_peak_price(self):
        logger.debug(findPeakStockByDays('000776',50))
