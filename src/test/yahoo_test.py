import unittest
from stocktrace.parse.yahooparser import parseFinanceData
from stocktrace import settings
from stocktrace.parse.yahooparser import downloadHistorialData

class TestSequenceFunctions(unittest.TestCase):
    def test_poll_ydn(self):
        parseFinanceData('600327')

    def test_yahoo(self):
        downloadHistorialData('600327',True)

    def test_pandas(self):
        import pandas as pd
        from stocktrace.dao.stockdao import findAllQuotes
        result = findAllQuotes()
        print result
        df = pd.DataFrame(list(result))
        print df
