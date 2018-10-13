from django.test import TestCase
from market.parse import *
from market.sh import avg_sh_pe
from stocktrace.dao.stockdao import *
from market.analysis import *
from market.csi import read_index, read_industry, read_index_all, read_industry_all, csi_by_type, read_index2
from market.csi import read_equity_by_date, read_equity, read_equity_all, read_equity_by_portfolio, read_equities
from market.xueqiu import read_portfolio, read_history, read_market, low_pb_ratio, high_pb_ratio, read_index_market, \
    high_price_ratio, gdp_rate
from market.sw import read_sw_all
from market.tushare import stock_list, profit, finance_report
from market.sina import *

# > \Workspace\stocktrace>python manage.py test market.tests.ParseTestCase.test_sh_pe


class ParseTestCase(TestCase):
    code = '600420'
    begin = '2011-05-04'


    def test_stock_list(self):
        stock_list()

    def test_xueqiu(self):
        s = xueqiu(self.code)
        print(s)

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

    def test_read_index2(self):
        read_index2('000016')
        read_index2('000300')
        read_index2('000905')

    def test_read_index_all(self):
        read_index_all('2018-02-24')

    def test_read_industry_all(self):
        read_industry_all('2017-10-25', '2018-01-23')

    def test_read_equity_by_date(self):
        read_equity_by_date('2012-10-09', '600436')

    def test_read_equity(self):
        read_equity('600420', '2018-08-16', '2018-08-17')

    def test_read_equity_all2(self):
        read_equity_all('2018-08-30')

    def test_read_equity_all(self):
        read_equity_by_portfolio('2018-04-16')

    def test_read_equities(self):
        equities = ['002450', '002739', '601801', '002475', '300133', '002230', '002558', '000063', '000997',
                    '002279', '300271', '002065', '002456', '600398', '002024', '002572', '002508', '600233',
                    '600519', '002304', '000568', '000768', '000625', '600893', '600685', '600482', '002594',
                    '600038', '002460', '000738', '002466', '600995', '600583', '601985', '601857', '601808',
                    '002353', ]
        read_equities(equities, self.begin, '2016-12-31')


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
        gdp = gdp_rate()
        print(gdp)

    def test_low_pb(self):
        print(low_pb_ratio())

    def test_high_pb(self):
        print(high_pb_ratio())

    def test_high_price(self):
        high_price_ratio()

    def test_history(self):
        # codes = ['600420', '600177', '000028', '300246', '601009', ]
        codes = ['600420', ]
        for code in codes:
            read_history(code, '2013-01-02')

    def test_index_history(self):
        for code in ['SH000001', 'SZ399001', 'SZ399005', 'SZ399006']:
            history_list = read_history(code)
            print(history_list)
            # for history in history_list:
            #     history.save()

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

    def test_alert(self):
        alert_high_diff()

    def test_read_portfolio(self):
        read_portfolio()

    def test_sh(self):
        sh()

    def test_profit(self):
        profit()

    def test_finance_report(self):
        finance_report()

    def test_index_market(self):
        read_index_market('SH000001')

    def test_market(self):
        read_market(0, 1395, str(date.today()))

    def test_missing_data(self):
        codes = {'603056', '002223', '600733', '131810', '600535', '300244', '002475', '601600', '159920', '300146', '600995', '000029', '000002', '002230', '601857', '002773', '513100', '300015', '300033', '601166', '399005', '600900', '601985', '000776', '300339', '600104', '600309', '603127', '601318', '601288', '002304', '002901', '300630', '600511', '600036', '601998', '601939', '600926', '300017', '300024', '162411', '002422', '002007', '300122', '601066', '600398', '300347', '300124', '601801', '000768', '600547', '600332', '600028', '603898', '300036', '300750', '600109', '300253', '601633', '601669', '002287', '600056', '001979', '600779', '600019', '510180', '603288', '600816', '300003', '002020', '600518', '600893', '601155', '600741', '600887', '002179', '002120', '000661', '603233', '600901', '600340', '000166', '002739', '399678', '399006', '603801', '000997', '600177', '601169', '601377', '000300', '000063', '000568', '510330', '600606', '002294', '399001', '601128', '600629', '601901', '600196', '000617', '000538', '601878', '600566', '600867', '002839', '601088', '600482', '601628', '510050', '600519', '000333', '600377', '601375', '601688', '000028', '000728', '600673', '600380', '600436', '600909', '603658', '300529', '300676', '600705', '000560', '601838', '601881', '000710', '000963', '159949', '600011', '600998', '300246', '600999', '603939', '601186', '159915', '000738', '000016', '600919', '600760', '300166', '600837', '300451', '601211', '601601', '601800', '000513', '600570', '300348', '600000', '510300', '300271', '300463', '002424', '601108', '600600', '601766', '002142', '300436', '002415', '601988', '600908', '204001', '002589', '601111', '002821', '002038', '300685', '603259', '513500', '000858', '601607', '601933', '000625', '600977', '002001', '300294', '002410', '510500', '000999', '600009', '601336', '002262', '600276', '300482', '510900', '600062', '300168', '002727', '002594', '603833', '002352', '603368', '000001', '000423', '000651', '300383', '002019', '601668', '002673', '600383', '603858', '600233', '600030', '600959', '002507', '601009', '601229', '002065', '002024', '159919', '600029', '300558', '600572', '000905', '603018', '600048', '000666', '601198', '601788', '600533', '300009', '603387', '603039', '603883', '600521', '603882', '002736', '600958', '601006', '000813', '002252', '002572', '601997', '601398', '002883', '159902', '600420', '300199', '600085', '600161', '601818', '601138', '002236', '002285', '600016', '600271', '601888', '002468', '603885', '600015', '600115', '601021', '002044', '300059', '601328', '600027'}
        print(len(codes))
        for code in codes:
            eq = Equity.objects(code=code, date='2018-08-30')
            if len(eq) == 0:
                print(code)

    def test_sina(self):
        codes = ['600420', '131810', '02799']
        get_real_time_list(codes)

    def test_read_all(self):
        begin = '2018-10-08'
        end = '2018-10-13'
        read_index_all(begin)
        read_industry_all(begin)
        read_sw_all(begin)
        # read_equity_all(begin, end)
        read_equity_by_portfolio(begin, end)
        hs_cei()
        # 上证50/沪深300/中证500历史PE
        read_index2('000016')
        read_index2('000300')
        read_index2('000905')
        # finance_report(2018, 2)