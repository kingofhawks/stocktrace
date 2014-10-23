from django.test import TestCase
#from unittest import TestCase
from dao import delete_stock,update_stock_price,update_stock_amount,add_tag,find_stocks_by_tag
from stocktrace.parse.sinaparser import getStock
from portfolio import import_portfolio


class TestDao(TestCase):
    code = '600573'

    def test_delete_stock(self):
        #delete_stock('Money')
        self.fail()

    def test_update_stock(self):
        code = '600583'
        #update_stock_price(code,5300)
        update_stock_amount(code,3800,9,8.5)

    def test_sina_api(self):
        print getStock(self.code)

    def test_import(self):
        import_portfolio('G:\Dropbox\django\wsgi\openshift\stock\TOP100_20140404.EBK','top100')

    def test_add_tag(self):
        add_tag(self.code,'top100')

    def test_find_by_tag(self):
        stocks = find_stocks_by_tag('top100')
        for stock in stocks:
            print stock

