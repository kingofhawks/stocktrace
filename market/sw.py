# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from pandas.util.testing import DataFrame
import pandas as pd
import numpy as np
import requests
import json
from datetime import timedelta, datetime
import arrow
from django.conf import settings

db = settings.DB


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
                'pagecount': 993,
                'timed': 1456667319778
        }
        url = 'http://www.swsindex.com/handler.aspx'
        res = requests.post(url, data=payload)
        data = res.text.replace('\'', '\"')
        print(data)
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

    if 'PE' not in df:
        return
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


def read_sw_all(begin_date, end_date, codes):
    if end_date is None:
        now = arrow.now()
        end_date = str(now.date())
    if codes is None:
        codes = ['801020', '801030', '801040', '801050', '801080',
                 '801110', '801120', '801130', '801140', '801150', '801160', '801170', '801180',
                 '801200', '801210', '801230',
                 '801710', '801720', '801730', '801740', '801750', '801760', '801770', '801780', '801790',
                 '801880', '801890']
    for code in codes:
        df = parse_sw_history2(begin_date, end_date, code=code)
        if df is not None and not df.empty:
            records = json.loads(df.T.to_json()).values()
            db.sw.insert(records)