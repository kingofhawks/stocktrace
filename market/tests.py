from django.test import TestCase
from parse import *
from stocktrace.parse.yahooparser import *
from stocktrace.dao.stockdao import *
from analysis import *
from cix import *

# > \Workspace\stocktrace>python manage.py test market.tests.ParseTestCase.test_sh_pe


class ParseTestCase(TestCase):
    code = '600029'

    def test_sina(self):
        sina(self.code)

    def test_xueqiu(self):
        xueqiu(self.code)

    def test_ah_ratio(self):
        ah_ratio(0.8)

    def test_ah(self):
        ah_history()

    def test_ah2(self):
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
        print low_pb_ratio()

    def test_high_pb(self):
        print high_pb_ratio()

    def test_high_price(self):
        high_price_ratio()

    def test_history(self):
        for code in ['600029','601111','600276','600196','002294','601933','601607','002422','002179','600030','601009']:
            history_list = xueqiu_history(code)
            for history in history_list:
                history.save()

    def test_index_history(self):
        for code in ['SH000001', 'SZ399001', 'SZ399005', 'SZ399006']:
            history_list = xueqiu_history(code)
            for history in history_list:
                history.save()

    def test_history_yahoo(self):
        download_history_data(self.code)

    def test_history_sh(self):
        download_history_data('000001.SS')

    def test_sw_low(self):
        df = parse_sw_history('2014-03-12', '2014-03-13')
        df_to_collection(df, 'sw')

    def test_sw_now(self):
        import arrow
        now = arrow.now()
        begin_date = str(now.date())
        parse_sw_history(begin_date)

    def test_sw_history(self):
        codes = ['801020', '801030', '801040', '801050', '801080',
                '801110', '801120', '801130', '801140', '801150', '801160', '801170', '801180',
                '801200', '801210', '801230',
                '801710', '801720', '801730', '801740', '801750', '801760', '801770', '801780', '801790',
                '801880', '801890']
        for code in codes:
            df = parse_sw_history2(begin_date='2005-01-01', code=code)
            df_to_collection(df, 'sw')

    def test_sw_history2(self):
        df = parse_sw_history2(begin_date='2015-01-01', code='801150')
        df_to_collection(df, 'sw')

    def test_sw_history3(self):
        df = parse_sw_history2(begin_date='2016-01-01', code='801150')
        print df
        records = json.loads(df.T.to_json()).values()
        print records

    def test_sw(self):
        sw()

    def test_cix(self):
        cix_data = cix()
        cix_data.save()



