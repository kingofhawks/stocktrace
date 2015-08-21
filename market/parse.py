# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from models import Market
import pandas as pd
import numpy as np
import xlrd
import requests
import arrow


#1 parse shanghai market overall
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
    # read html <table> to list of DataFrame
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


#2 parse PE/PB from 申万行业一级指数
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
#3 GDP data can save locally
def parse_securitization_rate():
    pass


#4 parse comment in last day
def parse_xue_qiu_comment_last_day(stock='SH600029', access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol={}&hl=0&source=all&sort=time&page=1&_=1439801060661'
    url = url.format(stock)
    payload = {'access_token': access_token}
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

    r = requests.get(url, params=payload, headers=headers )
    print r
    print r.json()
    comments = r.json().get('list')
    print comments
    print len(comments)
    now = arrow.now()
    print now
    today = now.date()
    print str(today)

    today_begin = arrow.get(str(today)+'T00:00+08:00')
    today_end = arrow.get(str(today)+'T23:59+08:00')

    count = 0
    for comment in comments:
        timestamp = long(comment.get('created_at'))/1000
        utc = arrow.get(timestamp)
        local = utc.to('local')
        # print local
        if today_begin < utc and utc < today_end:
            print '***comment when trading***{}'.format(local)
            count += 1
        else:
            print 'comment not when trading:{}'.format(local)
    print 'stock {} comment:{}'.format(stock, count)
    return count


# get comment between trading time
def parse_xue_qiu_comment(stock='SH600027', access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol={}&hl=0&source=all&sort=time&page=1&_=1439801060661'
    url = url.format(stock)
    payload = {'access_token': access_token}
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

    r = requests.get(url, params=payload, headers=headers )
    print r
    print r.json()
    comments = r.json().get('list')
    print comments
    print len(comments)
    now = arrow.now()
    print now
    today = now.date()
    print str(today)

    morning_begin = arrow.get(str(today)+'T09:30+08:00')
    morning_end = arrow.get(str(today)+'T11:30+08:00')
    print morning_begin
    print morning_end
    print morning_begin.timestamp
    print morning_end.timestamp

    afternoon_begin = arrow.get(str(today)+'T13:00+08:00')
    afternoon_end = arrow.get(str(today)+'T15:00+08:00')
    print afternoon_begin
    print afternoon_end
    print afternoon_begin.timestamp
    print afternoon_end.timestamp

    count = 0
    for comment in comments:
        timestamp = long(comment.get('created_at'))/1000
        utc = arrow.get(timestamp)
        local = utc.to('local')
        # print local
        if (morning_begin < utc and utc < morning_end) or (afternoon_begin < utc and utc < afternoon_end):
            print '***comment when trading***{}'.format(local)
            count += 1
        else:
            print 'comment not when trading:{}'.format(local)
    print 'stock {} comment:{}'.format(stock, count)
    return count


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
def screen_by_price(low=0.1, high=3, access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
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


# get stock count by market value
def screen_by_market_value(low, high=60000, access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=symbol&order=desc&current=ALL&pct=ALL&page=1&mc={}_{}&_=1438834686129'
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


# get stock count by PB
def screen_by_pb(low=0.1, high=1, access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=pb&order=desc&current=ALL&pct=ALL&page=1&pb={}_{}&_=1440168645679'
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


# get stock count by static PE
def screen_by_static_pe(low=1, high=10, access_token='e41712c72e25cff3ecac5bb38685ebd6ec356e9f'):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=pelyr&order=desc&current=ALL&pct=ALL&page=1&pelyr={}_{}&_=1440168752260'
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


#5 stock ratio with low price
def low_price_ratio():
    count = screen_by_price()
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


#6 stock ratio with high price
def high_price_ratio():
    count = screen_by_price(low=100, high=10000)
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


#7 stock ratio with high market value
def high_market_value_ratio():
    count = screen_by_market_value(rmb_exchange_rate()[1])
    total = screen_by_market_value(1)
    ratio = float(count)/total
    print 'count:{} total:{} ratio:{}'.format(count, total, ratio)
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
    if code.startswith('hk'):
        current = float(test[6])
    else:
        current = float(test[3])
    print current
    return current


# HK and USD to RMB exchange rate from boc.cn
def rmb_exchange_rate():
    # url = 'http://www.boc.cn/sourcedb/whpj/'
    # r = requests.get(url)
    # print r.content
    page = parse('http://www.boc.cn/sourcedb/whpj/').getroot()
    # result = etree.tostring(page)
    # print result
    tables = page.xpath("//table")

    # import lxml.html as H
    # doc = H.document_fromstring(result)
    # tables=doc.xpath("//table")

    # print len(tables)

    dfs = pd.read_html(etree.tostring(tables[1]), flavor='lxml')
    # print len(dfs)
    df = dfs[0]
    print df
    hk_to_rmb = df.iloc[8][5]
    usd_to_rmb = df.iloc[22][5]
    print 'hk_to_rmb:{}'.format(hk_to_rmb)
    print 'usd_to_rmb:{}'.format(usd_to_rmb)
    return hk_to_rmb, usd_to_rmb


# AH ratio
def ah_ratio(hk_rmb_change_rate, ah_pair=('600036', '03968'), ):
    current_a = sina(ah_pair[0])
    current_h = sina(ah_pair[1])*hk_rmb_change_rate
    ratio = current_a/current_h
    # ratio = current_h/current_a
    print ratio
    return ratio


#8 AH premium index: average of sample stock's AH ratio
def ah_premium_index(samples=[('600036', '03968'), ('600196', '02196'), ('601111', '00753')]):
    ratio_list = []
    hk_to_rmb = float(rmb_exchange_rate()[0])/100
    for sample in samples:
        ratio = ah_ratio(hk_to_rmb, sample)
        ratio_list.append(ratio)
    print ratio_list
    ah_index = np.mean(ratio_list)
    print ah_index
    return ah_index





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
    # sina('00168')
    # sina('02318')
    # ah_ratio()
    # ah_premium_index()
    # rmb_exchange_rate()
    # parse_xue_qiu_comment()
    # parse_xue_qiu_comment_last_day('SZ000963')
    # screen_by_market_value(600)
    # high_market_value_ratio()
    # screen_by_pb()
    screen_by_static_pe()