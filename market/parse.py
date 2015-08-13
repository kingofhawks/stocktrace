# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from models import Market
import pandas as pd
import numpy as np
import xlrd
import requests

# parse shanghai market overall
def parse_sh_market():
    page = parse('http://www.sse.com.cn/market/').getroot()
    # result = etree.tostring(page)
    # print result

    r = page.get_element_by_id('dateList')
    statistics = r.text_content().split()
    for word in statistics:
        print word

    market = Market(statistics[1], statistics[8], statistics[12], statistics[14])
    print market

# parse SZ market overall
def parse_sz_market():
        # url = 'http://www.szse.cn/main/marketdata/tjsj/jbzb/'
    # dfs = pd.read_html(url, flavor='lxml')
    # print dfs
    page = parse('http://www.szse.cn/main/marketdata/tjsj/jbzb/').getroot()
    # result = etree.tostring(page)
    # print result

    r = page.get_element_by_id('REPORTID_tab1')
    print etree.tostring(r)
    # read html to list of DataFrame
    dfs = pd.read_html(etree.tostring(r), flavor='lxml')
    # print dfs
    # print len(dfs)
    if len(dfs) >= 1:
        df = dfs[0]
        # print df
        total_market = df.iloc[10][1]
        volume = df.iloc[12][1]
        avg_price = df.iloc[13][1]
        pe = df.iloc[14][1]
        turnover_rate = df.iloc[15][1]
        market = Market(total_market, volume, turnover_rate, pe)
        print market
        # print df.index
        # print df.columns
        # print df.values
        # print df.describe()

# parse PE/PB from 申万行业一级指数
def parse_sw(day='20150729'):
    # url = 'http://www.swsindex.com/pedata/SwClassifyPePb_{}.xls'.format(day)

    url = 'sw.xls'
    df = pd.read_excel(url)
    # print df
    # print df.columns
    # print df.T

    # select 一级行业rows
    df = df[pd.isnull(df[u'二级行业名称'])]
    print df

    static_pe = u'静态市盈率'
    #sort by static PE
    df = df.sort(columns=static_pe, ascending=False)
    print df

    max_pe = df[static_pe].max()
    min_pe = df[static_pe].min()
    avg_pe = df[static_pe].mean()
    print 'PE max:{} min:{} average:{}'.format(max_pe, min_pe, avg_pe)

    columns = [u'一级行业名称', u'静态市盈率', u'市净率']
    max_pe_index = df.loc[df[static_pe] == max_pe].index
    min_pe_index = df.loc[df[static_pe] == min_pe].index
    print 'max_pe_index:{} min_pe_index:{}'.format(max_pe_index, min_pe_index)
    print df.loc[df[static_pe] == max_pe][columns]
    print df.loc[df[static_pe] == min_pe][columns]
    # print df[int(max_pe_index[0]): int(max_pe_index[0])+1]
    # print df[int(min_pe_index[0]): int(min_pe_index[0])+1]

    # get row count via those different ways
    # print len(df)
    # print len(df.values)
    # print len(df.index)
    # print df.shape

    pb = u'市净率'
    df = df.sort(columns=pb, ascending=False)
    print df

    max_pb = df[pb].max()
    min_pb = df[pb].min()
    avg_pb = df[pb].mean()
    print 'PB max:{} min:{} average:{}'.format(max_pb, min_pb, avg_pb)

    max_pb_index = df.loc[df[pb] == max_pb].index
    min_pb_index = df.loc[df[pb] == min_pb].index
    print 'max_pb_index:{} min_pb_index:{}'.format(max_pb_index, min_pb_index)
    print df.loc[df[pb] == max_pb][columns]
    print df.loc[df[pb] == min_pb][columns]
    # print df[int(max_pb_index[0]): int(max_pb_index[0])+1]
    # print df[int(min_pb_index[0]): int(min_pb_index[0])+1]


# TODO
def parse_securitization_rate():
    pass

# get access token for xueqiu.com
def login_xue_qiu():
    url = 'http://xueqiu.com/user/login'
    payload = {'username': 'kingofhawks@qq.com', 'areacode': 86, 'remember_me': 1,
               'password': '1FA727F4CFC8E494E55524897EEC631E'}
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

    r = requests.post(url, params=payload, headers=headers)
    response_headers = r.headers
    cookie = response_headers.get('set-cookie')
    print cookie
    words = cookie.split(';')
    # print words
    xq_r_token = words[3]
    # print xq_r_token
    access_token = xq_r_token.split('=')[1]
    print access_token
    return access_token

# get stock count by price
def get_stock_count_by_price(low=0.1, high=3, access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=symbol&order=desc&current={}_{}&pct=ALL&page=1&_=1438835212122'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    # print '*************url********************{}'.format(url2)
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    count = result.get('count')
    print count
    return count

# stock ratio with low price
def low_price_ratio():
    count = get_stock_count_by_price()
    total = get_stock_count_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio

# stock ratio with high price
def high_price_ratio():
    count = get_stock_count_by_price(low=100, high=10000)
    total = get_stock_count_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio

# sina real time API
def sina(code):
    if code.startswith('60') or code.startswith('51'):
        code = 'sh'+code
    elif len(code) == 5:
        code = 'hk'+code
    else:
        code = 'sz'+code
    url = "http://hq.sinajs.cn/list="+code
    r = requests.get(url)
    print r.text
    test = r.content.split(',')
    print test
    current = float(test[3])
    print current
    return current

# AH ratio
def ah_ratio():
    pass

if __name__ == '__main__':
    # parse_sh_market()
    # parse_sz_market()
    # parse_sw()
    # access_token = login_xue_qiu()
    # low_price_ratio()
    # high_price_ratio()
    # login_xue_qiu()
    # sina('600030')
    # sina('002294')
    sina('02601')

