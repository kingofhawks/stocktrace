# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from models import Market
import pandas as pd
import numpy as np
import xlrd
import requests
import arrow
from datetime import timedelta

# check xueqiu http cookie "xq_a_token"
xq_a_token = '956d8e7a7e5b0a34d2fb90df5096f4891df8b88b'


# 1 parse shanghai market overall
def parse_sh_market():
    page = parse('http://www.sse.com.cn/market/').getroot()
    # result = etree.tostring(page)
    # print result

    r = page.get_element_by_id('dateList')
    statistics = r.text_content().split()
    for word in statistics:
        print word

    market = Market('sh', statistics[1], float(statistics[8])/10000, statistics[12], statistics[14], date=statistics[2])
    print market
    return market


# average PE for shanghai
def avg_sh_pe():
    # Dec PE from 2000~201508
    pe_list = [42.42, 47.99, 49.92, 51.13, 54.02, 55.22, 58.21, 58.13, 54.83, 56.31, 59.89, 59.14,
               59.39, 56.82, 60.88, 60.99, 55.92, 56.55, 49.26, 42.14, 40.61, 38.84, 40.08, 37.59,
               34.31, 35.11, 37.16, 39.08, 38.75, 44.47, 42.4, 43.02, 40.4, 38.23, 36.46, 34.5,
               37.92, 38.2, 38.2, 38.53, 38.28, 36.13, 35.78, 34.37, 32.97, 32.51, 34, 36.64,
               38.91, 40.89, 42.49, 38.95, 28.73, 26.65, 26.49, 25.68, 26.75, 25.34, 25.69, 24.29,
               22.87, 24.99, 22.63, 22.28, 15.66, 15.98, 16.05, 16.92, 16.78, 15.72, 15.63, 16.38,
               17.61, 18, 17.72, 19.42, 19.69, 19.91, 20.03, 20.38, 21.41, 22.86, 26.13, 33.38,
               38.36, 39.62, 44.36, 53.33, 43.42, 42.74, 50.59, 59.24, 63.74, 69.64, 53.79, 59.24,
               49.4, 49.21, 39.45, 42.06, 25.89, 20.64, 20.93, 18.13, 18.68, 14.09, 15.23, 14.86,
               16.26, 17.01, 19.37, 20.21, 22.47, 25.36, 29.47, 23.04, 24.12, 26.03, 27.93, 28.78,
               26.24, 26.91, 27.54, 25.42, 19.93, 18.47, 19.86, 19.85, 20, 22.61, 21.51, 21.6,
               21.63, 22.56, 22.77, 22.74, 16.34, 16.49, 16.14, 15.42, 14.19, 14.96, 14.17, 13.41,
               14.01, 14.86, 13.86, 14.7, 12.67, 11.9, 11.29, 11.03, 11.25, 11.17, 10.71, 12.29,
               12.97, 12.89, 12.18, 11.89, 11.81, 10.16, 10.26, 10.8, 11.19, 11.05, 11.46, 10.99,
               10.57, 10.73, 10.66, 10.65, 9.76, 9.8, 10.58, 10.68, 11.48, 11.8, 13.14, 15.99,
               15.94, 16.57, 18.97, 22.55, 21.92, 20.92, 18.04, 15.81]

    dates = pd.date_range('20000131', periods=len(pe_list), freq='M')
    s = pd.Series(pe_list, dates)
    df = pd.DataFrame(s, index=dates, columns=['PE'])
    print df
    print 'SH PE min:{} max:{} average:{}'.format(df['PE'].min(), df['PE'].max(), df['PE'].mean())
    return df['PE'].min(), df['PE'].max(), df['PE'].mean()


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
        print df
        total_market = df.iloc[10][1]
        volume = df.iloc[12][1]
        avg_price = df.iloc[13][1]
        pe = df.iloc[14][1]
        turnover_rate = df.iloc[15][1]

        if type(total_market) == type(pd.NaT):
            total_market = 0
        if type(volume) == type(pd.NaT):
            volume = 0
        print 'total_market:{}'.format(total_market)
        print 'volume:{}'.format(volume)
        market = Market('sz', float(total_market)/100000000, float(volume)/100000000, turnover_rate, pe, 0)
        print market
        # print df.index
        # print df.columns
        # print df.values
        # print df.describe()
        return market


# 创业板 market overall
def parse_cyb_market():
    return parse_sz_market_common('cyb', 'http://www.szse.cn/main/chinext/scsj/jbzb/')
    #
    # page = parse('http://www.szse.cn/main/chinext/scsj/jbzb/').getroot()
    # # result = etree.tostring(page)
    # # print result
    #
    # r = page.get_element_by_id('REPORTID_tab1')
    # print etree.tostring(r)
    # # read html <table> to list of DataFrame
    # dfs = pd.read_html(etree.tostring(r), flavor='lxml')
    # # print dfs
    # # print len(dfs)
    # if len(dfs) >= 1:
    #     df = dfs[0]
    #     print df
    #     total_market = df.iloc[5][1]
    #     volume = df.iloc[7][1]
    #     pe = df.iloc[10][1]
    #     high_pe = df.iloc[10][3]
    #
    #     if type(total_market) == type(pd.NaT):
    #         total_market = 0
    #     if type(volume) == type(pd.NaT):
    #         volume = 0
    #
    #     market = Market('cyb', float(total_market)/100000000, float(volume)/100000000, 0, pe)
    #     print market
    #     return market
    #     # print df.index
    #     # print df.columns
    #     # print df.values
    #     # print df.describe()


# 中小板 market overall
def parse_zxb_market():
        return parse_sz_market_common('zxb', 'http://www.szse.cn/main/sme/xqsj/jbzb/')


# parse sz market util
def parse_sz_market_common(name, url):
    page = parse(url).getroot()

    r = page.get_element_by_id('REPORTID_tab1')
    print etree.tostring(r)
    # read html <table> to list of DataFrame
    dfs = pd.read_html(etree.tostring(r), flavor='lxml')
    if len(dfs) >= 1:
        df = dfs[0]
        print df
        tradable_shares = df.iloc[4][1]
        total_market = df.iloc[5][1]
        volume_money = df.iloc[7][1]
        volume = df.iloc[8][1]
        pe = df.iloc[10][1]
        high_pe = df.iloc[10][3]
        value = df.iloc[13][1]

        if isinstance(tradable_shares, type(pd.NaT)):
            tradable_shares = 0
        if type(total_market) == type(pd.NaT):
            total_market = 0
        if isinstance(volume_money, type(pd.NaT)):
            volume_money = 0
        if isinstance(volume, type(pd.NaT)):
            volume = 0

        # 换手率＝成交量÷当日实际流通量
        if tradable_shares == 0:
            turnover = 0
        else:
            turnover = float(volume)/float(tradable_shares)
        market = Market(name, float(total_market)/100000000, float(volume_money)/100000000, turnover, pe, value)
        print market
        return market


# market list
def market_list():
    sh = parse_sh_market()
    sz = parse_sz_market()
    cyb = parse_cyb_market()
    zxb = parse_zxb_market()

    markets = [sh, sz, cyb, zxb]
    print markets
    return markets


# 2 parse PE/PB from 申万行业一级指数
def parse_sw():
    for i in range(0, 4):
        print i
        now = arrow.now()
        print now
        print now.weekday()
        week_day = now-timedelta(i)
        day = week_day.format('YYYYMMDD')
        sw = parse_sw_with_day(day)
        if sw is not None:
            return sw


def parse_sw_with_day(day=None):
    if day is None:
        now = arrow.now()
        print now
        print now.weekday()
        week_day = now-timedelta(now.weekday()-4)
        day = week_day.format('YYYYMMDD')
        print day

    url = 'http://www.swsindex.com/pedata/SwClassifyPePb_{}.xls'.format(day)

    res = requests.get(url)
    if res.ok:
        print 'ok'
    else:
        print 'can not download url:{}'.format(url)
        return None

    # url = 'sw.xls'
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
    median_pe = df[static_pe].median()
    print 'PE max:{} min:{} average:{} median:{}'.format(max_pe, min_pe, avg_pe, median_pe)

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
    median_pb = df[pb].median()
    print 'PB max:{} min:{} average:{} median_pb:{}'.format(max_pb, min_pb, avg_pb, median_pb)

    max_pb_index = df.loc[df[pb] == max_pb].index
    min_pb_index = df.loc[df[pb] == min_pb].index
    # median_pb_index = df.loc[df[pb] == avg_pb].index
    print 'max_pb_index:{} min_pb_index:{}'.format(max_pb_index, min_pb_index)
    print df.loc[df[pb] == max_pb][columns]
    print df.loc[df[pb] == min_pb][columns]
    # print df.loc[df[pb] == median_pb_index][columns]
    # print df[int(max_pb_index[0]): int(max_pb_index[0])+1]
    # print df[int(min_pb_index[0]): int(min_pb_index[0])+1]
    return df


# 3 GDP data can save locally
def parse_securitization_rate():
    # 2014 GDP
    last_year_gdp = 636462.71
    sh = parse_sh_market()
    sz = parse_sz_market()
    gdp = float(sh.total_market_cap)+float(sz.total_market_cap)/100000000
    print gdp
    securitization_rate = gdp/last_year_gdp
    print 'securitization_rate:{.2f}'.format(securitization_rate)
    return securitization_rate


# 4 parse comment in last day
def parse_xue_qiu_comment_last_day(stock='SH600029', access_token=xq_a_token):
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
def parse_xue_qiu_comment(stock='SH600027', access_token=xq_a_token):
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
    headers = {'content-type': 'application/json',
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}

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
def screen_by_price(low=0.1, high=3, access_token=xq_a_token):
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
def screen_by_market_value(low, high=60000, access_token=xq_a_token):
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
def screen_by_pb(low=0.1, high=1, access_token=xq_a_token):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=pb&order=desc&current=ALL&pct=ALL&page=1&pb={}_{}&_=1440168645679'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    # print '*************url********************{}'.format(url2)
    headers = {'content-type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    print result
    count = result.get('count')
    print count
    return count


def low_pb_ratio():
    count = screen_by_pb()
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


def high_pb_ratio():
    count = screen_by_pb()
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


# get stock count by static PE
def screen_by_static_pe(low=1, high=10, access_token=xq_a_token):
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


# 5 stock ratio with low price
def low_price_ratio():
    count = screen_by_price()
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


# 6 stock ratio with high price
def high_price_ratio():
    count = screen_by_price(low=100, high=10000)
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    print ratio
    return ratio


# 7 stock ratio with high market value
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


# 8 AH premium index: average of sample stock's AH ratio
def ah_premium_index(samples=[('600036', '03968'), ('600196', '02196'), ('601111', '00753')]):
    samples = [('600585', '00914'), ('601318', '02318'), ('000002', '02202'),
               ('600036', '03968'), ('600600', '00168'), ('600196', '02196'),
               ('600030', '06030'), ('600028', '00386'), ('601601', '02601'),
               ('601628', '02628'), ('000063', '00763'), ('601398', '01398'),
               ('601939', '00939'), ('601288', '01288'), ('600837', '06837'),
               ('601607', '02607'), ('600011', '00902'), ('002202', '02208'),
               ('601988', '03988'), ('601818', '06818'), ('601336', '01336'),
               ('600027', '01071'), ('601088', '01088'), ('601328', '03328'),
               ('600016', '01988'), ('601998', '00998'), ('601186', '01186'),
               ('600332', '00874'), ('601766', '01766'), ('002594', '01211'),
               ('601857', '00857'), ('000039', '02039'), ('600362', '00358'),
               ('600012', '00995'), ('601633', '02333'), ('601800', '01800'),
               ('601333', '00525'), ('601111', '00753'), ('600875', '01072'),
               ('601390', '00390'), ('601898', '01898'), ('601899', '02899'),
               ('000898', '00347'), ('000157', '01157'), ('600585', '00317'),
               ('601992', '02009'), ('601600', '02600'), ('601991', '00991'),
               ('600115', '00670'), ('601808', '02883'), ('600871', '01033'),
               ('601727', '02727'), ('600188', '01171'), ('601238', '02238'),
               ('601919', '01919'), ('601866', '02866'), ('601618', '01618'),
               ('600026', '01138'), ('601880', '02880'), ('600874', '01065')]
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
    # parse_cyb_market()
    # parse_zxb_market()
    market_list()
    # avg_sh_pe()
    # parse_securitization_rate()
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
    # screen_by_static_pe()
    # low_pb_ratio()
