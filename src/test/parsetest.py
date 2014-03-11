'''
Created on 2012-6-8

@author: Simon
'''
import unittest

class ParseTest(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        print self.__class__.__name__
   
#    def test_shuffle(self):
#        from parse.yahooparser import parseFinanceData
#        print parseFinanceData('600327')
#
#        #print 'ok'
#        
#    def testTriggerNhNl(self):
#        from dao.stockdao import triggerNhNl
#        print triggerNhNl('600999')
        
#    def testFindStockMA(self):
#        from stocktrace.dao.stockdao import checkStockWithMA,getMa
#        from stocktrace.util import settings
#        print checkStockWithMA('600657',10,10,settings.HIGHER)
#        print checkStockWithMA('600657',10,10,settings.LOWER)
#        print getMa('600327',20,10)
#        from stocktrace.parse.screener import findByMa2
#        print findByMa2()
        
#    def testFindFromMemcache(self):
#        import sys
#        print sys.path
#        from stocktrace.dao.stockdao import findPeakStockByDays
#        #findPeakStockByDays('600327',10)
#        print '+0.12%'.lstrip('+').rstrip('%')
#        print float('+0.12%')
        
#    def testRedis(self):
#        import redis
#        r = redis.StrictRedis(host='172.25.21.16', port=6379, db=0)
#        r.set('foo', 'bar')
#        print r.get('foo')
        
    def testDownload(self):
        from stocktrace.parse.yahooparser import download_history_data
        from stocktrace.util import settings
        download_history_data('600327',engine =  settings.CSV_ENGINE)
        from datetime import date
        from datetime import timedelta
        print date.today()
        delta = timedelta(-1)
        begin = date.today()+delta
        print begin
        
  