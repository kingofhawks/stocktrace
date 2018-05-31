# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from pandas.util.testing import DataFrame
from market.models import Index, AhIndex, Industry, Equity, Market
import pandas as pd
import numpy as np
import requests
import json
from datetime import timedelta, datetime
import arrow
from stocktrace.stock import Stock, StockHistory
import tushare as ts
from PyQt5 import Qt
import sys
import xlrd
import zipfile
import io
from django.conf import settings

db = settings.DB
api_home = 'http://xueqiu.com'
# check xueqiu HTTP request cookie "xq_a_token"
xq_a_token = 'f11c55a10baf6b9692d1eeee153286d38e2ffe60'
headers = {'content-type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}


# 4 parse comment in last day
def parse_xue_qiu_comment_last_day(stock='SH600029', access_token=xq_a_token):
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol={}&hl=0&source=all&sort=time&page=1&_=1439801060661'
    url = url.format(stock)
    payload = {'access_token': access_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r
    # print r.json()
    comments = r.json().get('list')
    now = arrow.now()
    # print now
    today = now.date()
    # print str(today)

    today_begin = arrow.get(str(today)+'T00:00+08:00')
    today_end = arrow.get(str(today)+'T23:59+08:00')

    count = 0
    for comment in comments:
        timestamp = int(comment.get('created_at'))/1000
        utc = arrow.get(timestamp)
        local = utc.to('local')
        # print local
        if today_begin < utc < today_end:
            # print '***comment when trading***{}'.format(local)
            count += 1
        else:
            print(('comment not when trading:{}'.format(local)))
    # print 'stock {} comment:{}'.format(stock, count)
    return count


# get comment between trading time
def parse_xue_qiu_comment(stock='SH600027', access_token=xq_a_token):
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol={}&hl=0&source=all&sort=time&page=1&_=1439801060661'
    url = url.format(stock)
    payload = {'access_token': access_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r
    # print r.json()
    comments = r.json().get('list')
    # print comments
    # print len(comments)
    now = arrow.now()
    today = now.date()

    morning_begin = arrow.get(str(today)+'T09:30+08:00')
    morning_end = arrow.get(str(today)+'T11:30+08:00')
    # print morning_begin
    # print morning_end
    # print morning_begin.timestamp
    # print morning_end.timestamp

    afternoon_begin = arrow.get(str(today)+'T13:00+08:00')
    afternoon_end = arrow.get(str(today)+'T15:00+08:00')
    # print afternoon_begin
    # print afternoon_end
    # print afternoon_begin.timestamp
    # print afternoon_end.timestamp

    count = 0
    for comment in comments:
        timestamp = int(comment.get('created_at'))/1000
        utc = arrow.get(timestamp)
        local = utc.to('local')
        # print local
        if (morning_begin < utc < morning_end) or (afternoon_begin < utc < afternoon_end):
            # print '***comment when trading***{}'.format(local)
            count += 1
        else:
            print(('comment not when trading:{}'.format(local)))
    # print 'stock {} comment:{}'.format(stock, count)
    return count


# get access token for xueqiu.com
def login_xue_qiu():
    url = 'http://xueqiu.com/user/login'
    payload = {'username': 'kingofhawks@qq.com', 'areacode': 86, 'remember_me': 1,
               'password': '1FA727F4CFC8E494E55524897EEC631E'}

    r = requests.post(url, params=payload, headers=headers)
    response_headers = r.headers
    cookie = response_headers.get('set-cookie')
    # print cookie
    words = cookie.split(';')
    # print words
    xq_r_token = words[3]
    # print xq_r_token
    access_token = xq_r_token.split('=')[1]
    # print access_token
    return access_token


# get stock count by price
def screen_by_price(low=0.1, high=3, access_token=xq_a_token):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=symbol&order=desc&current={}_{}&pct=ALL&page=1&_=1438835212122'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    # print '*************url********************{}'.format(url2)
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    # print result
    count = result.get('count')
    stock_list = result.get('list')
    stocks = []
    if stock_list:
        for stock in stock_list:
            stocks.append(stock.get('symbol'))
    result_dict = {'count': count, 'stocks': stocks}
    # print result_dict
    return result_dict


# get stock count by market value
def screen_by_market_value(low, high=60000, access_token=xq_a_token):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=symbol&order=desc&current=ALL&pct=ALL&page=1&mc={}_{}&_=1438834686129'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    # print '*************url********************{}'.format(url2)
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    count = result.get('count')
    # print count
    return count


# get stock count by PB
def screen_by_pb(low=0, high=0.999, access_token=xq_a_token):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=pb&order=desc&current=ALL&pct=ALL&page=1&pb={}_{}&_=1440168645679'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    print('*************url********************{}'.format(url2))
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    # print(result)
    count = result.get('count')
    # print count
    # return count
    stock_list = result.get('list')
    stocks = []
    if stock_list:
        for stock in stock_list:
            name = stock.get('name')
            # 过滤掉退市股
            if name.endswith('退'):
                continue
            stocks.append(stock.get('symbol'))
    result_dict = {'count': count, 'stocks': stocks}
    print(result_dict)
    return result_dict


def low_pb_ratio():
    data = screen_by_pb()
    # print data
    count = data['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    # print 'low_pb_ratio:{} size:{}'.format(ratio, count)
    return ratio, data['stocks'], total


def high_pb_ratio():
    data = screen_by_pb(low=10, high=10000)
    count = data['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    # print 'high_pb_ratio:{} size:{}'.format(ratio, count)
    return ratio, data['stocks']


# get stock count by static PE
def screen_by_static_pe(low=1, high=10, access_token=xq_a_token):
    url = 'http://xueqiu.com/stock/screener/screen.json?category=SH&orderby=pelyr&order=desc&current=ALL&pct=ALL&page=1&pelyr={}_{}&_=1440168752260'
    payload = {'access_token': access_token}
    url2 = url.format(low, high)
    # print '*************url********************{}'.format(url2)
    r = requests.get(url2, params=payload, headers=headers)
    # print r.text
    # print r.content
    result = r.json()
    count = result.get('count')
    # print count
    return count


# 5 stock ratio with low price
def low_price_ratio():
    count = screen_by_price()
    total = screen_by_price(high=10000)
    ratio = float(count)/total
    # print ratio
    return ratio


# 6 stock ratio with high price
def high_price_ratio():
    count = screen_by_price(low=100, high=10000)['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    # print 'count:{} total:{} ratio:{}'.format(count, total, ratio)
    return ratio


# parse real time data from xueqiu
def xueqiu(code='SH600036', access_token=xq_a_token):
    if code.startswith('60') or code.startswith('51'):
        code = 'SH'+code
    elif len(code) == 5:
        code = 'HK'+code
    elif code == '999999' or code == '999998':
        return Stock(code=code, current=1)
    elif len(code) == 6:
        code = 'SZ'+code

    url = 'http://xueqiu.com/v4/stock/quote.json?code={}&_=1443253485389'
    url = url.format(code)
    payload = {'access_token': access_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r
    # print r.json()
    data = r.json().get(code)
    print(data)
    time = data.get('time')
    print(time)
    if time:
        # Wed Dec 27 14:59:59 +0800 2017
        time = arrow.get(time, 'ddd MMM DD HH:mm:ss Z YYYY')
        print(time)
        stock = Stock(code=code,
                      # name=data.get('name').encode("GB2312"),
                      current=data.get('current'), percentage=data.get('percentage'),
                      open_price=data.get('open'), high=data.get('high'), low=data.get('low'), close=data.get('close'),
                      low52week=data.get('low52week'), high52week=data.get('high52week'),
                      change=data.get('change'),
                      pb=data.get('pb'),
                      date=time.datetime)
        print(stock)
        return stock
    else:
        return None


# parse history data
def read_history(code='600036', begin_date=None, end_date=None):
    if begin_date is None:
        begin = arrow.get('2014-01-01')
    else:
        begin = arrow.get(begin_date)
        # print begin_date
    if end_date is None:
        end = arrow.now()
    else:
        end = arrow.get(end_date)
    if len(code) == 8:
        pass
    elif code.startswith('60') or code.startswith('51'):
        code = 'SH'+code
    elif len(code) == 5:
        code = 'HK'+code
    elif len(code) == 6:
        code = 'SZ'+code

    # url = '{}/stock/forchartk/stocklist.json?symbol={}&period=1day&type=normal&begin={}&end={}&_=1443694358741'
    url = '{}/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}'
    url = url.format(api_home, code, begin.timestamp*1000, end.timestamp*1000)
    print(url)
    payload = {'access_token': xq_a_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r.json()
    data_list = r.json().get('chartlist')
    # print data_list
    # print len(data_list)
    result = []
    for data in data_list:
        # print(data)
        time = data.get('time')
        time = arrow.get(time, 'ddd MMM DD HH:mm:ss Z YYYY')
        date = time.date
        # print time
        timestamp = time.timestamp*1000
        history = StockHistory(code=code, percent=data.get('percent'),
                               ma5=data.get('ma5'), ma10=data.get('ma10'), ma30=data.get('ma30'),
                               open_price=data.get('open'), high=data.get('high'), low=data.get('low'),
                               close=data.get('close'), time=time.datetime, timestamp=timestamp,
                               volume=data.get('volume'),
                               # 注：指数无法取得换手率
                               turn_rate=data.get('turnrate'))
        nh = False
        nl = False
        # if high == high52week:
        #     nh = True
        # if low == low52week:
        #     nl = True
        # Equity.objects(code=code, date=date).update_one(percent=data.get('percent'),
        #                        ma5=data.get('ma5'), ma10=data.get('ma10'), ma30=data.get('ma30'),
        #                        open_price=data.get('open'), high=data.get('high'), low=data.get('low'),
        #                        close=data.get('close'), time=time.datetime, timestamp=timestamp,
        #                        volume=data.get('volume'),
        #                        # 注：指数无法取得换手率
        #                        turn_rate=data.get('turnrate'), upsert=True)
        # print history
        result.append(history)
    df = DataFrame(data_list)
    # print df
    max_turnover = df['turnrate'].max()
    min_turnover = df['turnrate'].min()
    # print df['turnrate'].mean()
    # max_turnover_index = df.loc[df['turnrate'] == max_turnover].index
    # print max_turnover_index
    columns = ['time', 'turnrate', 'volume', 'close']
    # print df.loc[df['turnrate'] == max_turnover][columns]
    # print df.loc[df['turnrate'] == min_turnover][columns]
    max_volume = df['volume'].max()
    min_volume = df['volume'].min()
    mean_volume = df['volume'].mean()
    # print df.loc[df['volume'] == max_volume][columns]
    # print df.loc[df['volume'] == min_volume][columns]
    return result


def ah_history():
    read_history('HKHSAHP')


@DeprecationWarning
def stock_list():
    import tushare as ts
    df = ts.get_stock_basics()
    stocks = df.index.tolist()
    print((len(stocks)))
    print(stocks)
    for stock in stocks:
        s = Stock()
        s.code = stock
        s.save()


def read_portfolio():
    url = 'https://xueqiu.com/v4/stock/portfolio/list.json?system=true&_=1520056368754'
    payload = {'access_token': xq_a_token}
    r = requests.get(url, params=payload, headers=headers)
    # print(r.json())
    data = r.json()
    portfolios = data.get('portfolios')
    # print(portfolios)
    stock_set = set()
    for portfolio in portfolios:
        # print(portfolio)
        stocks = portfolio.get('portfolio').get('stocks')
        print(stocks)
        if stocks:
            stocks_list = stocks.split(',')
            print(stocks_list)
            for stock in stocks_list:
                if stock and len(stock) == 8:
                    import re
                    # remove SHZ character
                    line = re.sub('[SHZ]', '', stock)
                    stock_set.add(line)
    print(stock_set)
    return stock_set


def read_market(nh, nl, date):
    date_format = 'YYYY-MM-DD'
    day = arrow.get(date, date_format).date()
    low_pb = low_pb_ratio()
    print(low_pb)
    print('*'*20)
    broken_net_ratio = low_pb[0]
    broken_net = len(low_pb[1])
    stock_count = low_pb[2]
    nh_ratio = float(nh)/stock_count
    nl_ratio = float(nl)/stock_count

    Market.objects(date=day).update_one(nh=nh, nl=nl, nhnl=nh-nl, nh_ratio=nh_ratio, nl_ratio=nl_ratio,
                                        stock_count=stock_count,
                                        broken_net=broken_net, broken_net_ratio=broken_net_ratio,
                                        broken_net_stocks=low_pb[1],
                                        upsert=True)
