'''
Created on 2011-3-7

@author: simon
'''
import sys, traceback
from datetime import date
from datetime import datetime
from datetime import timedelta
from stocktrace.stock import Stock
from lxml import etree
from lxml.html import parse
from stocktrace.dao.stockdao import *
import io
from stocktrace.util import slf4p, settings
import requests

logger = slf4p.getLogger(__name__)

#TODO get xueqiu access token
# def get_access_token(code):
#     payload = {'access_token': 'zsviyNEZkM9JzOleP8iNIi', 'xq_r_token': 'P9xs0e4T0TOLzzMJvvoVEk'}
#
#     r = requests.post('https://xueqiu.com/service/poster', params=payload)
#     # r = requests.get('http://xueqiu.com/stock/quote.json?code='+code, auth=('kingofhawks@qq.com', 'lazio_2000'))
#     print r.json()


#codes: SH600583,SZ000728,GS
def parse_real_time(codes):
    #TODO get access token when login xueqiu
    payload = {'access_token': 'e41712c72e25cff3ecac5bb38685ebd6ec356e9f'}
    url = 'http://xueqiu.com/stock/quote.json?code='+codes
    print '*************url********************{}'.format(url)
    r = requests.get(url, params=payload)
    result = r.json()
    quotes = result.get('quotes')
    for quote in quotes:
        print 'quote:{}'.format(quote)
        code = quote.get('code')
        name = quote.get('name')
        current = quote.get('current')
        percentage = quote.get('percentage')
        open = quote.get('open')
        high = quote.get('high')
        low = quote.get('low')
        close = quote.get('close')
        last_close = quote.get('last_close')
        high52week = quote.get('high52week')
        low52week = quote.get('low52week')
        volume = quote.get('volume')
        marketCapital = quote.get('marketCapital')
        eps = quote.get('eps')
        pe_ttm = quote.get('pe_ttm')
        pe_lyr = quote.get('pe_lyr')
        beta = quote.get('beta')
        time = quote.get('time')
        net_assets = quote.get('net_assets')
        pb = quote.get('pb')
        psr = quote.get('psr')
        print 'high52week:{} low52week:{}'.format(high52week, low52week)
        percentFromYearLow = (float(current)-float(low52week))*100/float(low52week)
        percentFromYearHigh = (float(high52week)-float(current))*100/float(high52week)
        nh = False
        nl = False
        if high == high52week:
            nh = True
        if low == low52week:
            nl = True

        update_quote(code, current=float(current), year_high=float(high52week), year_low=float(low52week),
                     percentFromYearHigh=percentFromYearHigh, percentFromYearLow=percentFromYearLow,
                     nh=nh, nl=nl,
                     high=high, low=low, name=name)


#Update collection ticker with latest info
def update_quote(code, current, ma50=0.0, ma200=0.0, year_high=0.0, year_low=0.0, percentFromYearHigh=0.0,
                 percentFromYearLow=0.0, nh=False, nl=False, high=0.0, low=0.0, name=''):
    if len(code) == 8:
        code = code[2:]
        print '*******************update code******************************:{}'.format(code)
    ticker = db.tickers
    logger.info('{} current:{} yearLow:{} yearHigh:{} percentFromYearLow:{} percentFromYearHigh:{}'.format(code,current,year_high,year_low,percentFromYearLow,percentFromYearHigh))
    logger.info(ticker.update({"code": code},
    {"$set":{"current":current,"ma50":ma50,"ma200":ma200,"yearHigh":year_high,"yearLow":year_low,
             'high': high, 'low': low,'nh': nh, 'nl': nl,
             "percentFromYearHigh":percentFromYearHigh,"percentFromYearLow":percentFromYearLow,"name":name}},
    upsert=True,safe=True))


#download all statistics data
def download_statistics(stockList=settings.STOCK_LIST_TOP100):
    logger.info('Begin Download stock list data {}'.format(stockList))

    #download securities list from local
    from stocktrace.parse.sseparser import downloadQuoteList
    downloadQuoteList(True, False, stockList)
    quotes = find_all_tickers()
    print 'quotes:{}'.format(quotes)
    parse_real_time(','.join(quotes))
    # for quote in quotes:
    #     print 'quote:{}'.format(quote)
    #     if quote is None:
    #         pass
    #     parse_real_time(quote)

    logger.info( '****Download latest price from sina finished****')


