from django.test import TestCase
from parse import *


class ParseTest(TestCase):
    code = '600036'

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

    def test_gdp(self):
        parse_securitization_rate()

    def test_low_pb(self):
        low_pb_ratio()

    def test_high_pb(self):
        high_pb_ratio()


