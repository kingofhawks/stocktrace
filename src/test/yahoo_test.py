import unittest
from stocktrace.parse.yahooparser import parseFinanceData

class TestSequenceFunctions(unittest.TestCase):
    def test_yahoo(self):
        parseFinanceData('600327')
