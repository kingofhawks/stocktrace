from django.test import TestCase
from market.parse import *
from stocktrace.dao.stockdao import *
from market.analysis import *
from market.cix import *
from market.csi import read_index, read_industry, read_index_all, read_industry_all, csi_by_type
from market.csi import read_equity_by_date, read_equity, read_equity_all, read_equity_by_portfolio, read_equities
from market.xueqiu import read_portfolio, read_history
from market.sw import read_sw_all
# > \Workspace\stocktrace>python manage.py test market.tests.ParseTestCase.test_sh_pe


class ParseTestCase(TestCase):
    code = '600609'
    begin = '2011-05-04'

    def test_xueqiu(self):
        stock = xueqiu(self.code)
        if stock:
            stock.save()

    def test_ah(self):
        ah_history()

    def test_sh_pe(self):
        avg_sh_pe()

    def test_csi(self):
        csi('20170102')

    def test_csi_all(self):
        csi_all('20110503', '20170101')

    def test_csi_industry(self):
        csi_industry('20110503')

    def test_csi_industry_all(self):
        csi_industry_all('20170215', '20171231')

    def test_csi_by_type(self):
        csi_by_type('2018-02-23', 'zy1')

    def test_csi_by_type2(self):
        csi_by_type('2018-02-23', 'zz4')

    def test_read_index(self):
        read_index('2016-01-04')

    def test_read_index_all(self):
        read_index_all('2018-02-24')

    def test_read_industry_all(self):
        read_industry_all('2017-10-25', '2018-01-23')

    def test_read_equity_by_date(self):
        read_equity_by_date('2012-10-09', '600436')

    def test_read_equity(self):
        read_equity('000625', '2015-09-01', '2017-01-02')

    @DeprecationWarning
    def test_read_equity_all2(self):
        read_equity_all(self.begin, '2016-12-31')

    def test_read_equity_all(self):
        read_equity_by_portfolio('2018-04-16')

    def test_read_equities(self):
        equities = ['002450', '002739', '601801', '002475', '300133', '002230', '002558', '000063', '000997',
                    '002279', '300271', '002065', '002456', '600398', '002024', '002572', '002508', '600233',
                    '600519', '002304', '000568', '000768', '000625', '600893', '600685', '600482', '002594',
                    '600038', '002460', '000738', '002466', '600995', '600583', '601985', '601857', '601808',
                    '002353', ]
        read_equities(equities, self.begin, '2016-12-31')

    def test_read_all(self):
        begin = '2018-05-07'
        read_index_all(begin)
        read_industry_all(begin)
        read_sw_all(begin)
        # read_equity_all(begin)
        read_equity_by_portfolio(begin)
        hs_cei()

    def test_hscei(self):
        hs_cei()

    def test_hscei_daily(self):
        hs_cei_daily()

    def test_sz(self):
        market = parse_sz_market()
        if market:
            market.save()

    def test_szzb(self):
        market = parse_szzb_market()
        if market:
            market.save()

    def test_zxb(self):
        market = parse_zxb_market()
        if market:
            market.save()

    def test_cyb(self):
        market = parse_cyb_market()
        if market:
            market.save()

    def test_cyb2(self):
        parse_cyb2()

    def test_gdp(self):
        parse_securitization_rate()

    def test_low_pb(self):
        print(low_pb_ratio())

    def test_high_pb(self):
        print(high_pb_ratio())

    def test_high_price(self):
        high_price_ratio()

    def test_history(self):
        codes = ['600420', '600177', '000028', '300246', '601009', ]
        for code in ['600420']:
            history_list = read_history(code, '2018-02-03', '2018-05-04')
            print(history_list)

    def test_index_history(self):
        for code in ['SH000001', 'SZ399001', 'SZ399005', 'SZ399006']:
            history_list = xueqiu_history(code)
            for history in history_list:
                history.save()

    def test_read_sw_all(self):
        read_sw_all('2005-01-04', '2005-02-20')

    def test_read_sw(self):
        read_sw_all('2013-01-02', '2014-02-21', codes=['801780'])

    @DeprecationWarning
    def test_sw_history3(self):
        df = parse_sw_history2(begin_date='2016-01-01', code='801150')
        print(df)
        records = json.loads(df.T.to_json()).values()
        print(records)

    def test_sw(self):
        sw()

    def test_cix(self):
        cix_data = cix()
        cix_data.save()

    def test_alert(self):
        alert_high_diff()

    def test_read_portfolio(self):
        read_portfolio()

    def test_sh(self):
        sh()
