'''
Created on 2012-6-8

@author: Simon
'''
import unittest

class ParseTest(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)
        print self.__class__.__name__
   
    def test_shuffle(self):
        from parse.yahooparser import parseFinanceData
        print parseFinanceData('600327')

        #print 'ok'
        
    def testTriggerNhNl(self):
        from dao.stockdao import triggerNhNl
        print triggerNhNl('600327')
        
  