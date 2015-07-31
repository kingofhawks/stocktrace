# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
import pandas as pd
import xlrd


def parse_sw(day='20150729'):
    # url = 'http://www.swsindex.com/pedata/SwClassifyPePb_{}.xls'.format(day)

    url = 'sw.xls'
    df = pd.read_excel(url)
    # print df
    # print df.columns
    # print df.T

    static_pe = u'静态市盈率'

    #sort by static PE
    df.sort(columns=static_pe, ascending=False)
    # print df

    max_pe = df[static_pe].max()
    avg_pe = df[static_pe].mean()
    print max_pe
    print avg_pe

    max_pe_index = df.loc[df[static_pe] == max_pe].index
    print max_pe_index

    #get row count via those different ways
    print len(df)
    print len(df.values)
    print len(df.index)
    print df.shape


    pb = u'市净率'
    max_pb = df[pb].max()
    avg_pb = df[pb].mean()

    print max_pb
    print avg_pb


if __name__ == '__main__':
    parse_sw()
