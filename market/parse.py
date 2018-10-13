# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from pandas.util.testing import DataFrame
from market.models import Index, AhIndex, Industry, Equity
from market.utils import rmb_exchange_rate, get_excel_book
from market.xueqiu import xueqiu, read_history, read_index_market, screen_by_price
import pandas as pd
import numpy as np
import requests
import json
from datetime import timedelta, datetime
import arrow

from portfolio.models import get_stocks, get_stocks_from_latest_portfolio
from stocktrace.stock import Stock
import tushare as ts
from PyQt5 import Qt
import sys
import xlrd
import zipfile
import io
from django.conf import settings

db = settings.DB
# check xueqiu HTTP request cookie "xq_a_token"
xq_a_token = 'f11c55a10baf6b9692d1eeee153286d38e2ffe60'
headers = {'content-type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}


# 1 parse shanghai market overall
def parse_sh_market():
    page = parse('http://www.sse.com.cn/market/stockdata/overview/day/').getroot()
    result = etree.tostring(page)
    print(result)

    r = page.get_element_by_id('dateList')
    statistics = r.text_content().split()
    # for word in statistics:
    #     print word

    market = Index(name='sh', total_market_cap=statistics[1], volume=float(statistics[8]) / 10000,
                   turnover=statistics[12], pe=statistics[14], date=statistics[2])
    # print market
    return market


# 中证指数
@DeprecationWarning
def parse_sh_market2():
    url = 'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio?date=2017-12-29&type=zy1'
    page = parse(url).getroot()
    result = etree.tostring(page)
    print(result)
    el = page.xpath("//tbody[@class='tc']")
    print(el)
    for element in el:
        table = etree.tostring(element)
        print(table)
        dfs = pd.read_html(table, flavor='lxml')
        print(dfs)
    r = page.cssselect('tbody.tc')
    print(r[0].text_content())
    # res = requests.get(url, data=payload)
    # print(res.text)
    dfs = pd.read_html(r[0].text_content(), flavor='lxml')
    print(dfs)
    # print res.text
    # read html <table> to list of DataFrame
    # dfs = pd.read_html(res.text, flavor='lxml')


# extract zip file to memory file
def extract_zip(input_zip):
    return {name: input_zip.read(name) for name in input_zip.namelist()}


# 中证指数
def csi(date='20171228'):
    # http://115.29.204.48/syl/bk20180202.zip
    day = arrow.get(date,'YYYYMMDD').date()
    weekday = day.weekday()
    # ignore weekend
    if weekday == 5 or weekday == 6:
        return
    url = 'http://115.29.204.48/syl/bk'+date+'.zip'
    r = requests.get(url)
    if r.status_code == 404:
        return
    # create memory file
    z = zipfile.ZipFile(io.BytesIO(r.content))
    # not extract to disk file here
    # z.extractall()
    memory_unzip_files = extract_zip(z)
    # print(zip_files)
    # pandas read_csv not work!
    # df = pd.read_csv("bk20171228.csv")
    # xls_file = pd.ExcelFile('bk20171228.xls', encoding_override="gb2312")
    # xls_file = pd.read_excel('bk20171228.xls', encoding="gb2312")
    for name in memory_unzip_files.keys():
        book = xlrd.open_workbook(file_contents=memory_unzip_files.get(name), encoding_override="gbk")
        print("The number of worksheets is {0}".format(book.nsheets))
        print("Worksheet name(s): {0}".format(book.sheet_names()))
        for sheet in range(book.nsheets):
            sh = book.sheet_by_index(sheet)
            print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            for rx in range(sh.nrows):
                row = sh.row(rx)
                # print(row)
                name = row[0].value
                value = row[1].value
                print(name, value)
                # print(pe.replace('.', '', 1).isdigit(), type(pe))
                if value.replace('.', '', 1).isdigit():
                    if sheet == 0:
                        # 静态市盈率
                        Index.objects(name=name, date=day).update_one(name=name, date=day, pe=value, upsert=True)
                    elif sheet == 1:
                        # 滚动市盈率
                        print(Index.objects(name=name, date=day))
                        Index.objects(name=name, date=day).update_one(name=name, pe_ttm=value, upsert=True)
                    elif sheet == 2:
                        # 板块市净率
                        Index.objects(name=name, date=day).update_one(name=name, pb=value, upsert=True)
                    elif sheet == 3:
                        # 板块股息率
                        Index.objects(name=name, date=day).update_one(name=name, dividend_yield_ratio=value, upsert=True)
    # book = xlrd.open_workbook("bk"+date+".xls", encoding_override="gbk")
    # print("The number of worksheets is {0}".format(book.nsheets))
    # print("Worksheet name(s): {0}".format(book.sheet_names()))
    # sh = book.sheet_by_index(0)
    # print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
    # for rx in range(sh.nrows):
    #     row = sh.row(rx)
    #     # print(row)
    #     name = row[0].value
    #     pe = row[1].value
    #     # print(name, pe)
    #     # print(name, pe)
    #     # print(pe.replace('.', '', 1).isdigit(), type(pe))
    #     if pe.replace('.', '', 1).isdigit():
    #         market = Market(name=name, pe=pe)
    #         print(market)


def csi_all(begin_date='20171228', end_date=None):
    date_format = 'YYYYMMDD'
    if end_date is None:
        end_date = arrow.now().format(date_format)
    begin_arrow = arrow.get(begin_date, date_format)
    begin = begin_arrow.date()
    end = arrow.get(end_date, date_format).date()
    delta = end-begin
    print(delta.days)
    for i in range(delta.days):
        day = begin_arrow.shift(days=i).format(date_format)
        csi(day)


# 中证指数行业/个股PE
def csi_industry(date='20180212'):
    # http://115.29.204.48/syl/csi20180212.zip
    day = arrow.get(date, 'YYYYMMDD').date()
    weekday = day.weekday()
    # ignore weekend
    if weekday == 5 or weekday == 6:
        return
    url = 'http://115.29.204.48/syl/csi'+date+'.zip'
    r = requests.get(url)
    if r.status_code == 404:
        return
    # create memory file
    z = zipfile.ZipFile(io.BytesIO(r.content))
    # not extract to disk file here
    memory_unzip_files = extract_zip(z)
    for name in memory_unzip_files.keys():
        file_contents = memory_unzip_files.get(name)
        if len(file_contents) == 0:
            db.log.insert({'date': date})
            continue
        if file_contents:
            book = xlrd.open_workbook(file_contents=memory_unzip_files.get(name), encoding_override="gbk")
            print("The number of worksheets is {0} for date {}".format(book.nsheets), date)
            # print("Worksheet name(s): {0}".format(book.sheet_names()))
            for sheet in range(book.nsheets):
                sh = book.sheet_by_index(sheet)
                print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
                for rx in range(sh.nrows):
                    row = sh.row(rx)
                    # print(row)
                    code = row[0].value
                    name = row[1].value
                    value = row[2].value
                    if value.replace('.', '', 1).isdigit():
                        if sheet == 0:
                            # 行业静态市盈率
                            Industry.objects(code=code, date=day).update_one(code=code, date=day, name=name, pe=value, upsert=True)
                        elif sheet == 1:
                            # 行业滚动市盈率
                            Industry.objects(code=code, date=day).update_one(code=code, pe_ttm=value, upsert=True)
                        elif sheet == 2:
                            # 行业市净率
                            Industry.objects(code=code, date=day).update_one(code=code, pb=value, upsert=True)
                        elif sheet == 3:
                            # 行业股息率
                            Industry.objects(code=code, date=day).update_one(code=code, dividend_yield_ratio=value, upsert=True)
                        elif sheet == 4:
                            # 个股数据
                            code1 = row[2].value
                            code2 = row[4].value
                            code3 = row[6].value
                            code4 = row[8].value
                            row10 = row[10].value
                            row11 = row[11].value
                            row12 = row[12].value
                            row13 = row[13].value
                            try:
                                pe = float(row10)
                            except:
                                pe = 0

                            try:
                                pe_ttm = float(row11)
                            except:
                                pe_ttm = 0

                            try:
                                pb = float(row12)
                            except:
                                pb = 0

                            try:
                                dyr = float(row13)
                            except:
                                dyr = 0
                            Equity.objects(name=name, date=day).update_one(code=code, date=day, name=name,
                                                                           code1=code1, code2=code2, code3=code3,
                                                                           code4=code4,
                                                                           pe=pe, pe_ttm=pe_ttm, pb=pb,
                                                                           dividend_yield_ratio=dyr, upsert=True)

def csi_industry_all(begin_date='20171228', end_date=None):
    date_format = 'YYYYMMDD'
    if end_date is None:
        end_date = arrow.now().format(date_format)
    begin_arrow = arrow.get(begin_date, date_format)
    begin = begin_arrow.date()
    end = arrow.get(end_date, date_format).date()
    delta = end-begin
    for i in range(delta.days):
        day = begin_arrow.shift(days=i).format(date_format)
        csi_industry(day)


# H股指数monthly
# TODO
def hs_cei():
    # url = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/dl_centre/reports_stat/monthly/pe/hscei.xls'
    url = 'https://www.hsi.com.hk/static/uploads/contents/en/dl_centre/monthly/pe/hscei.xls'
    # r = requests.get(url)
    # file_contents = io.BytesIO(r.content)
    # book = xlrd.open_workbook(file_contents=file_contents.read())
    book = get_excel_book(url)
    # print(book)
    name = 'HSCEI'
    for sheet in range(book.nsheets):
        sh = book.sheet_by_index(sheet)
        for rx in range(sh.nrows):
            row = sh.row(rx)
            # df = DataFrame(row)
            # print(df)
            # print(row)
            date = row[0].value
            pe = row[1].value
            # print(type(pe))
            if date and pe and type(pe) == float:
                py_date = xlrd.xldate.xldate_as_datetime(date, book.datemode)
                # print(py_date)
                date = str(py_date)
                print(pd.to_datetime(date))
                Index.objects(name=name, date=date).update_one(name=name, date=date, pe=pe, upsert=True)


def hs_cei_daily():
    url = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_9Feb18.csv'
    # TODO
    df = pd.read_csv(url)
    print(df)


# parse SZ market overall
def parse_sz_market():
    page = parse('http://www.szse.cn/main/marketdata/tjsj/jbzb/').getroot()

    r = page.get_element_by_id('REPORTID_tab1')
    # print etree.tostring(r)
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

        if type(total_market) == type(pd.NaT):
            total_market = 0
        if type(volume) == type(pd.NaT):
            volume = 0
        if type(turnover_rate) == type(pd.NaT):
            turnover_rate = 0
        if type(pe) == type(pd.NaT):
            pe = 0
        # print 'total_market:{} volume:{} turnover_rate:{} pe:{}'.format(total_market, volume, turnover_rate, pe)
        market = Index('sz', total_market_cap=float(total_market) / 100000000, volume=float(volume) / 100000000,
                       turnover=float(turnover_rate), pe=float(pe))
        print(market)
        # print df.index
        # print df.columns
        # print df.values
        # print df.describe()
        return market


# 深圳主板
def parse_szzb_market():
    return parse_sz_market_common('szzb', 'http://www.szse.cn/main/mainboard/scsj/jbzb/')


# 创业板 market overall
def parse_cyb_market():
    return parse_sz_market_common('cyb', 'http://www.szse.cn/main/chinext/scsj/jbzb/')


# 创业板指数
def parse_cyb2(url='http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.5328349224291742'):
    payload = {'ACTIONID': 7, 'AJAX': 'AJAX-TRUE','CATALOGID':'1898_nm','TABKEY':'tab1','txtQueryDate':'2016-01-15','REPORT_ACTION':'reach'}
    res = requests.post(url, data=payload)
    # print res.text
    # read html <table> to list of DataFrame
    dfs = pd.read_html(res.text, flavor='lxml')
    # dfs = pd.read_html(etree.tostring(r), flavor='bs4')
    if len(dfs) >= 1:
        df = dfs[0]
        # print df
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
        if isinstance(pe, type(pd.NaT)):
            pe = 0
        if type(value) != float:
            value = 0.0

        # 换手率＝成交量÷当日实际流通量
        if tradable_shares == 0:
            turnover = 0
        else:
            turnover = float(volume)/float(tradable_shares)
        # print 'name:{} total_market:{} volume:{} turnover:{} pe:{} value:{}'.format(name,
        #                                                                            total_market, volume_money,
        #                                                                            turnover, pe, value)
        market = Index('CYB', float(total_market) / 100000000, float(volume_money) / 100000000, turnover, pe, value)
        # print market
        return market


# 中小板 market overall
def parse_zxb_market():
        return parse_sz_market_common('zxb', 'http://www.szse.cn/main/sme/xqsj/jbzb/')


# parse sz market util
def parse_sz_market_common(name, url):
    page = parse(url).getroot()
    # result = etree.tostring(page)
    # print '*'*20
    # print result
    # print '*'*20

    r = page.get_element_by_id('REPORTID_tab1')
    # print '*'*20
    # print etree.tostring(r)
    # print '*'*20
    # read html <table> to list of DataFrame
    dfs = pd.read_html(etree.tostring(r), flavor='lxml')
    # dfs = pd.read_html(etree.tostring(r), flavor='bs4')
    if len(dfs) >= 1:
        df = dfs[0]
        print(df)
        tradable_shares = df.iloc[4][1]
        total_market = df.iloc[5][1]
        volume_money = df.iloc[7][1]
        volume = df.iloc[8][1]
        pe = df.iloc[10][1]
        # high_pe = df.iloc[10][3]
        # value = df.iloc[13][1]

        if isinstance(tradable_shares, type(pd.NaT)):
            tradable_shares = 0
        if type(total_market) == type(pd.NaT):
            total_market = 0
        if isinstance(volume_money, type(pd.NaT)):
            volume_money = 0
        if isinstance(volume, type(pd.NaT)):
            volume = 0
        if isinstance(pe, type(pd.NaT)):
            pe = 0
        # if type(value) != float:
        #     value = 0.0

        # 换手率＝成交量÷当日实际流通量
        if tradable_shares == 0:
            turnover = 0
        else:
            turnover = float(volume)/float(tradable_shares)
        # print 'name:{} total_market:{} volume:{} turnover:{} pe:{} value:{}'.format(name,
        #                                                                            total_market, volume_money,
        #                                                                            turnover, pe, value)
        market = Index(name, float(total_market) / 100000000, float(volume_money) / 100000000, turnover, pe)
        # print market
        return market


# market list
def market_list():
    sh = parse_sh_market()
    sz = parse_sz_market()
    cyb = parse_cyb_market()
    zxb = parse_zxb_market()

    markets = [sh, sz, cyb, zxb]
    # print markets
    return markets


# 2 parse PE/PB from 申万行业一级指数
def parse_sw():
    for i in range(0, 4):
        # print i
        now = arrow.now()
        # print now
        # print now.weekday()
        week_day = now-timedelta(i)
        day = week_day.format('YYYYMMDD')
        sw = parse_sw_with_day(day)
        if sw is not None:
            return sw


def parse_sw_with_day(day=None):
    if day is None:
        now = arrow.now()
        # print now
        # print now.weekday()
        week_day = now-timedelta(now.weekday()-4)
        day = week_day.format('YYYYMMDD')
        # print day

    url = 'http://www.swsindex.com/pedata/SwClassifyPePb_{}.xls'.format(day)
    static_pe = '静态市盈率'
    pb = '市净率'

    res = requests.get(url)
    if res.ok:
        print('ok')
    else:
        # print 'can not download url:{}'.format(url)
        return None

    # url = 'sw.xls'
    df = pd.read_excel(url)
    # print df
    # print df.columns
    # print df.T

    # select PB<1
    df2 = df.copy()
    df2 = df2[df2[pb] < 1]
    # print df2

    # select PB>10
    df3 = df.copy()
    df3 = df3[df3[pb] > 10]
    # print df3

    # select PE<10
    df4 = df.copy()
    df4 = df4[df4[static_pe] < 10]
    # print df4

    # select PE>100
    df5 = df.copy()
    df5 = df5[df5[static_pe] > 100]
    # print df5
    ##### end of PB/PE check ######

    # select 一级行业, ignore 二级行业
    df = df[pd.isnull(df['二级行业名称'])]
    # print df

    #sort by static PE
    df = df.sort(columns=static_pe, ascending=False)
    # print '******DataFrame sort by PE:{}'.format(df)

    max_pe = df[static_pe].max()
    min_pe = df[static_pe].min()
    avg_pe = df[static_pe].mean()
    median_pe = df[static_pe].median()
    # print 'PE max:{} min:{} average:{} median:{}'.format(max_pe, min_pe, avg_pe, median_pe)

    columns = ['一级行业名称', '静态市盈率', '市净率']
    max_pe_index = df.loc[df[static_pe] == max_pe].index
    min_pe_index = df.loc[df[static_pe] == min_pe].index
    # print 'max_pe_index:{} min_pe_index:{}'.format(max_pe_index, min_pe_index)
    # print df.loc[df[static_pe] == max_pe][columns]
    # print df.loc[df[static_pe] == min_pe][columns]
    # print df[int(max_pe_index[0]): int(max_pe_index[0])+1]
    # print df[int(min_pe_index[0]): int(min_pe_index[0])+1]

    # get row count via those different ways
    # print len(df)
    # print len(df.values)
    # print len(df.index)
    # print df.shape


    df = df.sort(columns=pb, ascending=False)
    # print '******DataFrame sort by PB:{}'.format(df)

    max_pb = df[pb].max()
    min_pb = df[pb].min()
    avg_pb = df[pb].mean()
    median_pb = df[pb].median()
    # print 'PB max:{} min:{} average:{} median_pb:{}'.format(max_pb, min_pb, avg_pb, median_pb)

    max_pb_index = df.loc[df[pb] == max_pb].index
    min_pb_index = df.loc[df[pb] == min_pb].index
    # median_pb_index = df.loc[df[pb] == avg_pb].index
    # print 'max_pb_index:{} min_pb_index:{}'.format(max_pb_index, min_pb_index)
    # print df.loc[df[pb] == max_pb][columns]
    # print df.loc[df[pb] == min_pb][columns]
    # print df.loc[df[pb] == median_pb_index][columns]
    # print df[int(max_pb_index[0]): int(max_pb_index[0])+1]
    # print df[int(min_pb_index[0]): int(min_pb_index[0])+1]
    return df


# parse history PE/PB from 申万一级行业
@DeprecationWarning
def parse_sw_history(begin_date='2014-03-12', end_date=None, codes=None):
    if end_date is None:
        now = arrow.now()
        end_date = str(now.date())
    if codes is None:
        codes = ('801010', '801020', '801030', '801040', '801050', '801060', '801070', '801080', '801090',
                 '801100', '801110', '801120', '801130', '801140', '801150', '801160', '801170', '801180', '801190',
                 '801200', '801210', '801220', '801230',
                 '801710', '801720', '801730', '801740', '801750', '801760', '801770', '801780', '801790',
                 '801880', '801890')
    condition = 'swindexcode in {} and BargainDate>=\'{}\' and BargainDate<=\'{}\''
    where = condition.format(codes, begin_date, end_date)
    # print where
    all_data = []
    for index in range(1, 1000):
        payload = {'tablename':'swindexhistory',
                'key': 'id',
                'p': index,
                'where': where,
                'orderby': 'swindexcode asc,BargainDate_1',
                'fieldlist': 'SwIndexCode,SwIndexName,BargainDate,CloseIndex,BargainAmount,Markup,'
                               'TurnoverRate,PE,PB,MeanPrice,BargainSumRate,DP',
                'pagecount': 28,
                'timed': 1453385628267
            }
        url = 'http://www.swsindex.com/handler.aspx'
        res = requests.post(url, data=payload)
        data = res.text.replace('\'', '\"')
        result = json.loads(data)
        data_list = result.get('root')
        # print 'url****'+url
        # print len(data_list)
        if len(data_list) == 0:
            break
        else:
           all_data.extend(data_list)
    df = DataFrame(all_data)
    df[['PE', 'PB']] = df[['PE', 'PB']].astype(float)
    # df['PE'] = df['PE'].astype(float)
    # df['PB'] = df['PB'].astype(float)
    # print '*'*20
    # print len(df)
    # print df
    df = df.sort(columns='PE', ascending=True)
    # print df
    df = df.sort(columns='PB', ascending=True)
    # print df
    # print 'PE mean:{}'.format(df['PE'].mean())
    # print 'PB mean:{}'.format(df['PB'].mean())
    # print 'PB<1:{}'.format(df[df.PB < 1])
    return df


def parse_sw_history2(begin_date='2014-03-12', end_date=None, code='801150'):
    if end_date is None:
        now = arrow.now()
        end_date = str(now.date())
    condition = 'swindexcode=\'{}\' and BargainDate>=\'{}\' and BargainDate<=\'{}\' and type=\'Day\''
    where = condition.format(code, begin_date, end_date)
    all_data = []
    for index in range(1, 1000):
        payload = {'tablename':'V_Report',
                'key': 'id',
                'p': index,
                'where': where,
                'orderby': 'swindexcode asc,BargainDate_1',
                'fieldlist': 'SwIndexCode,SwIndexName,BargainDate,CloseIndex,BargainAmount,Markup,'
                               'TurnoverRate,PE,PB,MeanPrice,BargainSumRate,DP',
                'pagecount': 1,
                'timed': 1456667319778
        }
        url = 'http://www.swsindex.com/handler.aspx'
        res = requests.post(url, data=payload)
        data = res.text.replace('\'', '\"')
        # print data
        result = json.loads(data)
        data_list = result.get('root')
        # print 'url****'+url
        # print len(data_list)
        if len(data_list) == 0:
            break
        else:
           all_data.extend(data_list)
    df = DataFrame(all_data)
    # print df
    # print df.info()
    # print df.describe()
    # print df['PE']
    # print df[df['BargainDate'] == '2015-10-16 0:00:00']

    # clean data with empty PE or PB
    df = df[df['PE'] != '']
    df = df[df['PB'] != '']

    # convert string to datetime(timestamp)
    df['BargainDate'] = pd.to_datetime(df['BargainDate'])

    # convert string to float
    df[['PE', 'PB']] = df[['PE', 'PB']].astype(float)
    print(df)
    # df_sort_pe = df.sort(columns='PE', ascending=True)
    df_sort_pe = df.sort_values(by='PE', ascending=True)
    # print df_sort_pe
    # df_sort_pb = df.sort(columns='PB', ascending=True)
    df_sort_pb = df.sort_values(by='PB', ascending=True)
    # print df_sort_pb
    # print 'PE mean:{}'.format(df['PE'].mean())
    # print 'PB mean:{}'.format(df['PB'].mean())
    # print 'PB<1:{}'.format(df[df.PB < 1])
    return df


# 3 GDP data can save locally
def parse_securitization_rate():
    # 2014 GDP
    last_year_gdp = 636462.71
    sh = parse_sh_market()
    sz = parse_sz_market()
    total_market = float(sh.total_market_cap)+float(sz.total_market_cap)
    # print total_market
    securitization_rate = total_market/last_year_gdp
    # print 'securitization_rate:{0:.2f}'.format(securitization_rate)
    return securitization_rate


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
        if today_begin < utc and utc < today_end:
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
        if (morning_begin < utc and utc < morning_end) or (afternoon_begin < utc and utc < afternoon_end):
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


# get stock price position
def position(code):
    current = sina(code)
    count = screen_by_price(current, high=60000)
    # print count


# AH ratio
def ah_ratio(hk_rmb_change_rate, ah_pair=('000002', '02202'), ):
    current_a = sina(ah_pair[0]).current
    current_h = sina(ah_pair[1]).current
    if current_a * current_h == 0:
        return None

    current_h_rmb = current_h * hk_rmb_change_rate
    ratio = current_a/current_h_rmb
    result = {'price_a': current_a, 'price_h': current_h, 'ratio': ratio}
    # print 'ah_ratio:{}'.format(result)
    return result


def ah_history():
    read_history('HKHSAHP')


# 8 AH premium index: average of sample stock's AH ratio
# AH history https://xueqiu.com/S/HKHSAHP
@DeprecationWarning
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
               ('000898', '00347'), ('000157', '01157'), ('600685', '00317'),
               ('601992', '02009'), ('601600', '02600'), ('601991', '00991'),
               ('600115', '00670'), ('601808', '02883'), ('600871', '01033'),
               ('601727', '02727'), ('600188', '01171'), ('601238', '02238'),
               ('601919', '01919'), ('601866', '02866'), ('601618', '01618'),
               ('600026', '01138'), ('601880', '02880'), ('600874', '01065'),
               ('600660', '03606'), ('600377', '00177'), ('000776', '01776'),
               ('601688', '06886'), ('000338', '02338'), ('600029', '01055'),
               ('603993', '03993'), ('601005', '01053'), ('600688', '00338'),
               ('600548', '00548'), ('002672', '00895'), ('000513', '01513'),
               ('000488', '01812'), ('601107', '00107'), ('601588', '00588'),
               ('600808', '00323'), ('000921', '00921'), ('600775', '00553'),
               ('600860', '00187'), ('000756', '00719'), ('601038', '00038'),
               ('600806', '00300'), ('002490', '00568'), ('002703', '01057'),
               ('600876', '01108'), ('601717', '00564'), ('000585', '00042')]
    a_list = []
    h_list = []
    price_a_list = []
    price_h_list = []
    ratio_list = []
    hk_to_rmb = float(rmb_exchange_rate()[0])/100
    for sample in samples:
        ratio = ah_ratio(hk_to_rmb, sample)
        if ratio:
            a_list.append(sample[0])
            h_list.append(sample[1])
            price_a_list.append(ratio.get('price_a'))
            price_h_list.append(ratio.get('price_h'))
            ratio_list.append(ratio.get('ratio'))
    df_dict = {'A': a_list, 'Price_A': price_a_list, 'H': h_list, 'Price_H': price_h_list, 'ratio': ratio_list}
    # print df_dict
    df = DataFrame(df_dict)
    # print df
    df = df.sort(columns='ratio', ascending=True)
    # print df
    # ah_index = np.mean(ratio_list)
    ah_index = df['ratio'].mean()
    # print 'ah_index:{}'.format(ah_index)
    # print 'discount stock:{}'.format(df[df.ratio < 1])
    return AhIndex(ah_index)


def alert_high_diff():
    # df = ts.get_realtime_quotes('600196')
    df = ts.get_realtime_quotes(['600196', '600519', '300482'])
    print((df[['code', 'name', 'price', 'b1_v', 'b1_p', 'a1_v', 'a1_p']]))
    for index, row in df.iterrows():
        # 差价超过0.1%就预警
        if ((float(row['a1_p'])-float(row['b1_p']))/float(row['price'])) >= 0.001:
            print((row["name"], row["b1_p"]))
            app = Qt.QApplication(sys.argv)
            systemtray_icon = Qt.QSystemTrayIcon(Qt.QIcon('/path/to/image'))
            systemtray_icon.show()
            systemtray_icon.showMessage('Title', row["name"])


def polling():
    result = []

    # 交易时间才需要刷新
    now = arrow.now()
    today = now.date()
    weekday = now.weekday()

    trade_begin = arrow.get(str(today)+'T09:25+08:00')
    trade_end = arrow.get(str(today)+'T19:30+08:00')
    refresh = False
    if trade_begin < now < trade_end:
        refresh = True
    # ignore weekend
    if weekday == 5 or weekday == 6:
        refresh = False
    stocks = get_stocks_from_latest_portfolio()
    for item in stocks:
        code = item['code']
        amount = item['amount']
        current = item.get('current')
        if amount <= 0:
            continue
        if True:
            s = xueqiu(code)
            print('code:{} s:{}'.format(code, s))
            Stock.objects(code=code).update_one(code=code, amount=amount, current=s.current, volume=s.volume,
                                                percentage=s.percentage, change=s.change,
                                                open_price=s.open_price, high=s.high, low=s.low, close=s.close,
                                                high52week=s.high52week, low52week=s.low52week,
                                                nh=s.nh, nl=s.nl, upsert=True)
        stock = Stock.objects.get(code=code)
        stock.amount = amount
        if stock.current is None and current:
            stock.current = current
        result.append(stock)
    return result


# now work!
def sh():
    url = 'http://query.sse.com.cn/marketdata/tradedata/queryNewMonthlyTrade.do?jsonCallBack=jsonpCallback47165&prodType=gp&inYear=2018-02&_=1520055711697'
    payload = {'PHPStat_Cookie_Global_User_Id': '_ck16010722352115983758577133685'}
    r = requests.get(url, params=payload, headers=headers)
    print(r.text)
    print(r.json())