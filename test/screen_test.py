import unittest
from stocktrace.util import slf4p,settings
from stocktrace.stock import Stock,download_stock
from stocktrace.parse.screener import findByNhnl

logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600583'
    sh = Stock('600327')
    sz = Stock('002236')
    # 601318

    def test_nhnl(self):
        logger.debug(findByNhnl())
