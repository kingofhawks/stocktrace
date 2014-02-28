import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace import settings
from stocktrace.parse.yahooparser import downloadHistorialData
from stocktrace.util import slf4p
logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    def test_poll_ydn(self):
        parseFinanceData('600327')

    def test_yahoo(self):
        downloadHistorialData('600327',True)

    def test_pandas(self):
        import pandas as pd
        from stocktrace.dao.stockdao import findAllQuotes,findStockByCode
        result = findStockByCode('600327')
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
