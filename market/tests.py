from django.test import TestCase
from parse import *
from stocktrace.parse.yahooparser import *
from stocktrace.dao.stockdao import *

# > \Workspace\stocktrace>python manage.py test market.tests.ParseTestCase.test_sh_pe


class ParseTestCase(TestCase):
    code = '002294'

    def test_sina(self):
        sina(self.code)

    def test_xueqiu(self):
        xueqiu(self.code)

    def test_ah_ratio(self):
        ah_ratio(0.8)

    def test_ah(self):
        ah = ah_premium_index()
        ah.save()

    def test_sh_pe(self):
        avg_sh_pe()

    def test_cyb(self):
        parse_cyb_market()

    def test_cyb2(self):
        parse_cyb2()

    def test_zxb(self):
        parse_zxb_market()

    def test_gdp(self):
        parse_securitization_rate()

    def test_low_pb(self):
        low_pb_ratio()

    def test_high_pb(self):
        high_pb_ratio()

    def test_high_price(self):
        high_price_ratio()

    def test_history(self):
        history_list = xueqiu_history(self.code)
        for history in history_list:
            history.save()

    def test_history_yahoo(self):
        download_history_data(self.code)

    def test_sw_low(self):
        df = parse_sw_history('2014-03-12', '2014-03-13')
        df_to_collection(df, 'sw')

    def test_sw_now(self):
        import arrow
        now = arrow.now()
        begin_date = str(now.date())
        parse_sw_history(begin_date)

    def test_sw_history(self):
        df = parse_sw_history('2005-01-01')
        df_to_collection(df, 'sw')

    def test_sw_history2(self):
        df = parse_sw_history2('2015-01-01', '2016-01-01')
        df_to_collection(df, 'sw')


