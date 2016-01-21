from django.test import TestCase
from parse import *

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
        ah_premium_index()

    def test_sh(self):
        parse_sh_market()

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

    def test_history(self):
        xueqiu_history(self.code)

    def test_sw(self):
        parse_sw_history()


