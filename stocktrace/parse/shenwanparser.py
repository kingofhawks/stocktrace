# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
import pandas as pd
import xlrd

def parse_sw(day='20150729'):
    # url = 'http://www.swsindex.com/pedata/SwClassifyPePb_{}.xls'.format(day)

    url = 'sw.xls'
    df = pd.read_excel(url)
    print df
    print df.columns
    max_pe = df[u'静态市盈率'].max()
    print max_pe

    # df.loc[df.col == max_pe].index
    # print r.columns
    # print len(r.values)


if __name__ == '__main__':
    parse_sw()
