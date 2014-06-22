import unittest
from stocktrace.parse.sinaparser import getStock
from stocktrace.parse.yahooparser import download_history_data
from stocktrace.util import slf4p,settings
from stocktrace.parse.sinaparser import update
from stocktrace.stock import Stock,download_stock
from stocktrace.parse.screener import findByNhnl

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600583'
    sh = Stock('600327')
    sz = Stock('002236')
    # 601318

    def test_sina_api(self):
        logger.debug(getStock(self.code))
