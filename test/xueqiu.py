import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace.parse.yahooparser import download_history_data
from stocktrace.dao.stockdao import findAllQuotes,findStockByCode,find_week52_history,update_week52,remove_stock
from stocktrace.util import slf4p,settings
from stocktrace.parse.sinaparser import update
from stocktrace.stock import Stock,download_stock
from stocktrace.data.download import download2
from stocktrace.parse import xueqiuparser

logger = slf4p.getLogger(__name__)


class XueQiuTestCase(unittest.TestCase):
    code = 'SH600583'
    sh = Stock('600327')
    sz = Stock('SZ002236')

    def test_print_stock(self):
        xueqiuparser.parse_real_time('SH600583,SZ000728,GS,SH000001')
        # xueqiuparser.parse_real_time('SH600011')
        print self.sh

    def test_download(self):
        xueqiuparser.download_statistics()

