import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace import settings
from stocktrace.parse.yahooparser import downloadHistorialData
from stocktrace.dao.stockdao import findAllQuotes,findStockByCode,find_week52_history,update_week52
from stocktrace.util import slf4p
from stocktrace.parse.sinaparser import update
logger = slf4p.getLogger(__name__)

class TestSequenceFunctions(unittest.TestCase):
    code = '600327'

    def test_poll_ydn(self):
        parseFinanceData(self.code)

    def test_yahoo_csv(self):
        downloadHistorialData(self.code,True)

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
