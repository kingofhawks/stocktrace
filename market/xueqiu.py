# -*- coding:utf-8 -*-
import re

import pymongo
from dateutil.tz import tzutc
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
from numpy import interp
from market.sh import avg_sh_pe
from market.utils import rmb_exchange_rate, get_date
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
xq_a_token = '97465d3b59dcabc762005b4418a3c48007979082'
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
def comment(stock='SH600027'):
    url = 'http://xueqiu.com/statuses/search.json?count=15&comment=0&symbol={}&hl=0&source=all&sort=time&page=1&_=1439801060661'
    url = url.format(stock)
    payload = {'access_token': xq_a_token}

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
    print(result)
    count = result.get('count')
    stock_list = result.get('list')
    stocks = []
    ts_count = 0
    if stock_list:
        for stock in stock_list:
            name = stock.get('name')
            # 不包含退市股
            if name and '退' not in name:
                stocks.append(stock.get('symbol'))
            elif name and '退' in name:
                ts_count += 1
    result_dict = {'count': count-ts_count, 'stocks': stocks}
    print(result_dict)
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
                count -= 1
                continue
            stocks.append(stock.get('symbol'))
    result_dict = {'count': count, 'stocks': stocks}
    # print(result_dict)
    return result_dict


def low_pb_ratio():
    data = screen_by_pb()
    # print data
    count = data['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    # print 'low_pb_ratio:{} size:{}'.format(ratio, count)
    return ratio, count, data['stocks'], total


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


def screen_by_pencentage(low=-10.11, high=-9.9, access_token=xq_a_token):
    url = 'https://xueqiu.com/stock/screener/screen.json?category=SH&exchange=&areacode=&indcode=&orderby=symbol&order=desc&current=ALL&pct={}_{}&page=1&_=1528891053799'
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
def low_price_ratio(price=3):
    count = screen_by_price(low=0.1, high=price)['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    return ratio


# 6 stock ratio with high price
def high_price_ratio(price=100):
    count = screen_by_price(low=price, high=10000)['count']
    total = screen_by_price(high=10000)['count']
    ratio = float(count)/total
    return count, ratio


# parse real time data from xueqiu
def xueqiu(code='SH600036', access_token=xq_a_token):
    if code.startswith('60') or code.startswith('51'):
        code = 'SH'+code
    elif len(code) == 5:
        code = code
    elif code == '999999' or code == '999998':
        return Stock(code=code, current=1)
    elif len(code) == 6:
        code = 'SZ'+code

    url = api_home+'/v4/stock/quote.json?code={}&_=1443253485389'
    url = url.format(code)
    print(url)
    payload = {'access_token': access_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r
    # print r.json()
    data = r.json().get(code)
    print('data:{} code:{}'.format(data, code))
    if data:
        # Wed Dec 27 14:59:59 +0800 2017
        stock = Stock(code=code,
                     # name=data.get('name').encode("GB2312"),
                      current=data.get('current'), percentage=data.get('percentage'),
                      open_price=data.get('open'), high=data.get('high'), low=data.get('low'), close=data.get('close'),
                      low52week=data.get('low52week'), high52week=data.get('high52week'),
                      change=data.get('change'),
                      pb=data.get('pb'))
        time = data.get('time')
        print(time)
        if time:
            time = arrow.get(time, 'ddd MMM DD HH:mm:ss Z YYYY')
            print(time)
            stock.date = time.datetime
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

    code2 = code
    if len(code) == 8:
        pass
    elif code.startswith('60') or code.startswith('51'):
        code2 = 'SH'+code
    elif len(code) == 5:
        code2 = 'HK'+code
    elif len(code) == 6:
        code2 = 'SZ'+code

    # url = '{}/stock/forchartk/stocklist.json?symbol={}&period=1day&type=normal&begin={}&end={}&_=1443694358741'
    url = '{}/stock/forchartk/stocklist.json?symbol={}&period=1day&type=before&begin={}&end={}'
    url = url.format(api_home, code2, begin.timestamp*1000, end.timestamp*1000)
    # print(url)
    payload = {'access_token': xq_a_token}

    r = requests.get(url, params=payload, headers=headers)
    print(r.json())
    data_list = r.json().get('chartlist')
    # print data_list
    # print len(data_list)
    result = []
    for data in data_list:
        print(data)
        time = data.get('time')
        time = arrow.get(time, 'ddd MMM DD HH:mm:ss Z YYYY')
        date = time.format('YYYY-MM-DD')
        # print('date:{}'.format(date))
        # timestamp = time.timestamp*1000
        # history = StockHistory(code=code, percent=data.get('percent'),
        #                        ma5=data.get('ma5'), ma10=data.get('ma10'), ma30=data.get('ma30'),
        #                        open_price=data.get('open'), high=data.get('high'), low=data.get('low'),
        #                        close=data.get('close'), time=time.datetime, timestamp=timestamp,
        #                        volume=data.get('volume'),
        #                        # 注：指数无法取得换手率
        #                        turn_rate=data.get('turnrate'))
        # print(Equity.objects(code=code, date=date))
        Equity.objects(code=code, date=date).update_one(percent=data.get('percent'),
                                                        open=data.get('open'), high=data.get('high'),
                                                        low=data.get('low'),
                                                        close=data.get('close'), volume=data.get('volume'), upsert=True)
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
        # result.append(history)
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


# SZ399001+SH000001+SZ399006+SZ399005/last year GDP
def gdp_rate():
    # last year GDP http://data.eastmoney.com/cjsj/gdp.html
    last_year_gdp = 827121.70*1e8
    sh = read_index_market('SH000001')
    print(sh)
    sz = read_index_market('SZ399001')
    print(sz)
    sz = read_index_market('SZ399001')
    print(sz)
    zxb = read_index_market('SZ399005')
    print(zxb)
    cyb = read_index_market('SZ399006')
    print(cyb)
    total_market = float(sh.get('market_capital'))+float(sz.get('market_capital'))+float(zxb.get('market_capital'))+float(cyb.get('market_capital'))
    print(total_market)
    securitization_rate = total_market/last_year_gdp
    # print 'securitization_rate:{0:.2f}'.format(securitization_rate)
    return securitization_rate


def read_market(nh, nl, date):
    # 破净率
    low_pb = low_pb_ratio()
    print(low_pb)
    broken_net_ratio = low_pb[0]
    broken_net = low_pb[1]
    stock_count = low_pb[3]
    nh_ratio = float(nh)/stock_count
    nl_ratio = float(nl)/stock_count

    # 跌停板
    dt = screen_by_pencentage(-10.11, -9.9)
    dt_ratio = dt/stock_count
    # 涨停板
    zt = screen_by_pencentage(9.9, 10.11)
    zt_ratio = zt/stock_count
    zdr = zt-dt
    print('dtb:{} ztb:{} zdr'.format(dt, zt, zdr))

    # 仙股
    penny_stocks = screen_by_price(0.1, 1)['count']
    penny_stocks_ratio = penny_stocks/stock_count

    #  破发率
    broken_ipo_count, total_ipo, broken_ipo_rate, broken_list = broken_ipo()

    # CIX范围从0到100,由10个指标组成
    cix = 0
    weight_range = [0, 10]

    # 1 SH PE
    pe_df = avg_sh_pe('2000-1-31')
    max_pe = pe_df['PE'].max()
    min_pe = pe_df['PE'].min()
    # get latest PE DF by tail()
    # latest_pe_df = pe_df.tail(1)
    # latest_pe = latest_pe_df.iloc[0][1]
    # print 'latest PE:{}'.format(latest_pe)
    latest_sh = Index.objects(name='上海A股').order_by('-date').first()
    print('items***{}'.format(latest_sh))
    pe = interp(latest_sh.pe, [min_pe, max_pe], weight_range)
    # print('min_pe:{} max_pe:{} latest_pe:{} pe:{}'.format(min_pe, max_pe, latest_pe, pe))
    cix += pe

    # 2 破净率
    min_low_pb = 0
    max_low_pb = 0.1
    pb = interp(-broken_net_ratio, [-max_low_pb, min_low_pb], weight_range)
    cix += pb

    # 3 AH premium index
    ah_now = xueqiu('HKHSAHP')
    ah_current = ah_now.current
    ah = interp(ah_current, [100, 150], weight_range)
    cix += ah

    # 4 GDP rate
    rate = gdp_rate()
    gdp = interp(rate, [0.4, 1], weight_range)
    cix += gdp

    # 5 百元股 [0,3.6%]
    high_price = high_price_ratio()
    g100 = high_price[0]
    g100_ratio = high_price[1]
    high = interp(g100_ratio, [0, 0.036], weight_range)
    cix += high

    # 5 SH换手率 [1%,3%]
    sh = read_index_market('SH000001')
    turnover_rate = sh['turnover_rate']
    turnover = interp(turnover_rate, [1, 3], weight_range)
    cix += turnover

    # 6 涨跌停差额


    # 7 TODO 最近一年IPO、可转债涨幅或破发率


    # 8 TODO NHNL

    # 9 融资规模及占比

    # 10 社交媒体挖掘


    # TODO low price
    low_price = low_price_ratio()
    print('low_price***{}'.format(low_price))

    # TODO cix 映射到0.5-1.5区间,代表持仓比例
    Market.objects(date=get_date(date)).update_one(nh=nh, nl=nl, nhnl=nh-nl, nh_ratio=nh_ratio, nl_ratio=nl_ratio,
                                                   stock_count=stock_count,
                                                   over_100=g100, over_100_ratio=g100_ratio,
                                                   penny_stocks=penny_stocks, penny_stocks_ratio=penny_stocks_ratio,
                                                   low_price_ratio=low_price,
                                                   pe=latest_sh.pe, turnover=turnover_rate,
                                                   ah=ah_current, gdp=rate, cix=cix,
                                                   broken_net=broken_net, broken_net_ratio=broken_net_ratio,
                                                   broken_net_stocks=low_pb[2],
                                                   dt=dt, dt_ratio=dt_ratio, zt=zt, zt_ratio=zt_ratio, zdr=zdr,
                                                   ipo=total_ipo, broken_ipo=broken_ipo_count,
                                                   broken_ipo_ratio=broken_ipo_rate,broken_ipo_list=broken_list,
                                                   upsert=True)


# 指数市值
def read_index_market(code):
    url = 'https://stock.xueqiu.com/v5/stock/quote.json?symbol='+code
    payload = {'access_token': xq_a_token}
    r = requests.get(url, params=payload, headers=headers)
    # print(r.json())
    data = r.json()
    # print(data)
    quote = data.get('data').get('quote')
    print(quote)
    return quote


# 7 stock ratio with high market value
def high_market_value_ratio():
    count = screen_by_market_value(rmb_exchange_rate()[1])
    total = screen_by_market_value(1)
    ratio = float(count)/total
    # print 'count:{} total:{} ratio:{}'.format(count, total, ratio)
    return ratio


# 雪球新股行情
def ipo(page=1):
    # all columns
    all_columns = 'symbol,name,onl_subcode,list_date,actissqty,onl_actissqty,onl_submaxqty,onl_subbegdate,onl_unfrozendate,onl_refunddate,iss_price,onl_frozenamt,onl_lotwinrt,onl_lorwincode,onl_lotwiner_stpub_date,onl_effsubqty,onl_effsubnum,onl_onversubrt,offl_lotwinrt,offl_effsubqty,offl_planum,offl_oversubrt,napsaft,eps_dilutedaft,leaduwer,list_recomer,acttotraiseamt,onl_rdshowweb,onl_rdshowbegdate,onl_distrdate,onl_drawlotsdate,first_open_price,first_close_price,first_percent,first_turnrate,stock_income,onl_lotwin_amount,listed_percent,current,pe_ttm,pb,percent,hasexist'
    columns = 'name,onl_subcode,list_date,iss_price,current,symbol,onl_subbegdate,actissqty'
    url = 'https://xueqiu.com/proipo/query.json?page={}&size=30&order=desc&orderBy=list_date&stockType=&type=quote&_=1539863464075&column={}'.format(page, columns)
    payload = {'access_token': xq_a_token}
    r = requests.get(url, params=payload, headers=headers)
    data = r.json().get('data')
    date_format = 'ddd MMM DD HH:mm:ss Z YYYY'

    for stock in data:
        print(stock)
        name = stock[0]
        # code = stock[1]
        list_date = stock[2]
        # CST(China Standard Time timezone解析有问题，转化一下)
        list_date = list_date.replace('CST', '+0800')
        print(list_date)
        date = arrow.get(list_date, date_format)
        print(date.datetime)
        issue_price = stock[3]
        current = stock[4]
        symbol = stock[5]
        subscribe_date = stock[6]
        sub_date = None
        if subscribe_date and "CST" in subscribe_date:
            subscribe_date = subscribe_date.replace('CST', '+0800')
            sub_date = arrow.get(subscribe_date, date_format).datetime
            print(sub_date)
        issue_amount = stock[7]
        financing = 0
        if issue_price and issue_amount:
            financing = float(issue_price)*float(issue_amount)
        code = re.sub('[SHZ]', '', symbol)
        break_point_rate = 0
        if issue_price and float(current) < float(issue_price):
            break_point_rate = (current-issue_price)/issue_price
            print(break_point_rate)
        Stock.objects(code=code).update_one(code=code, name=name, list_date=date.datetime, sub_date=sub_date, issue_price=issue_price,
                                            current=current, break_point_rate=break_point_rate,
                                            issue_amount=issue_amount, financing=financing, upsert=True)


def ipo_all(begin_page=1, end_page=92):
    for page in range(begin_page, end_page):
        ipo(page+1)


def broken_ipo(begin='2018-01-01', end='2018-12-31'):
    begin_date = arrow.get(begin + 'T00:00+08:00')
    end_date = arrow.get(end + 'T00:00+08:00')
    documents = db.stock.find({"list_date": {"$gte": begin_date.datetime, "$lte": end_date.datetime}}).sort([("list_date", pymongo.DESCENDING)])
    stocks = list(documents)
    print(stocks)
    total_ipo = len(stocks)
    print(total_ipo)
    broken_ipo_count = 0
    broken_list = []
    for stock in list(stocks):
        if stock.get('break_point_rate') < 0:
            print(stock)
            broken_ipo_count += 1
            broken_list.append(stock.get('name'))
    broken_ipo_rate = broken_ipo_count/total_ipo
    return broken_ipo_count, total_ipo, broken_ipo_rate, broken_list
