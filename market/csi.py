# -*- coding:utf-8 -*-
from lxml import etree
from lxml.html import parse
from pandas.util.testing import DataFrame
from market.models import Index, Industry, Equity
import pandas as pd
import numpy as np
import requests
import json
from datetime import timedelta, datetime
import arrow
import xlrd
import zipfile
import io
from django.conf import settings

db = settings.DB
date_format = 'YYYY-MM-DD'
csi_domain = 'http://www.csindex.com.cn/zh-CN/downloads/'


# 中证指数(主要板块/行业)
def csi_by_type(date='2011-05-04', data_type='zy1'):
    # http://115.29.204.48/syl/bk20180202.zip
    day = arrow.get(date, date_format).date()
    weekday = day.weekday()
    # ignore weekend
    if weekday == 5 or weekday == 6:
        return
    url = '{}industry-price-earnings-ratio?date={}&type={}'.format(csi_domain, date, data_type)
    print('url***', url);
    page = parse(url).getroot()
    # result = etree.tostring(page)
    # print(result)
    xpath = '//table[@class="table  table-bg p_table table-bordered table-border mb-20"]'
    if data_type == 'zz1' or data_type == 'zz2' or data_type == 'zz3' or data_type == 'zz4':
        xpath = '//table[@class="table table-bg p_table table-bordered table-border mb-20"]'
    r = page.xpath(xpath)
    # print(len(r))
    tree = etree.ElementTree(r[0])
    # print(etree.tostring(tree))
    html_table = etree.tostring(tree)
    dfs = pd.read_html(html_table, flavor='lxml')
    df = dfs[0]
    print(df)
    # v1 = df.iloc[3][0]
    # print(v1, df.iloc[3][1], df.iloc[3][2])
    # print(v1, df.iloc[4][1], df.iloc[4][2])
    for index, row in df.iterrows():
        v0 = row.iloc[0]
        v1 = row.iloc[1]
        v2 = row.iloc[2]
        # print(index, name, value)
        print('index {} v0:{} v1:{} v2:{}***'.format(index, v0, v1, v2))
        try:
            if data_type == 'zy1':
                # 静态市盈率
                Index.objects(name=v0, date=day).update_one(name=v0, pe=v1, upsert=True)
            elif data_type == 'zy2':
                # 滚动市盈率
                Index.objects(name=v0, date=day).update_one(name=v0, pe_ttm=v1, upsert=True)
            elif data_type == 'zy3':
                # 市净率
                Index.objects(name=v0, date=day).update_one(name=v0, pb=v1, upsert=True)
            elif data_type == 'zy4':
                # 股息率
                Index.objects(name=v0, date=day).update_one(name=v0, dividend_yield_ratio=v1, upsert=True)
            elif data_type == 'zz1':
                # 行业静态市盈率
                Industry.objects(code=v0, date=day).update_one(code=v0, date=day, name=v1, pe=v2, upsert=True)
            elif data_type == 'zz2':
                # 行业滚动市盈率
                Industry.objects(code=v0, date=day).update_one(code=v0, pe_ttm=v2, upsert=True)
            elif data_type == 'zz3':
                # 行业市净率
                Industry.objects(code=v0, date=day).update_one(code=v0, pb=v2, upsert=True)
            elif data_type == 'zz4':
                # 行业股息率
                Industry.objects(code=v0, date=day).update_one(code=v0, dividend_yield_ratio=v2, upsert=True)
        except:
            continue


def csi(date='2011-05-04'):
    csi_by_type(date, 'zy1')
    csi_by_type(date, 'zy2')
    csi_by_type(date, 'zy3')
    csi_by_type(date, 'zy4')
    csi_by_type(date, 'zz1')
    csi_by_type(date, 'zz2')
    csi_by_type(date, 'zz3')
    csi_by_type(date, 'zz4')


def csi_all(begin_date='2017-12-28', end_date=None):
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


# 中证指数(个股)
def read_equity_by_date(date='2018-02-23', code='600420'):
    # http://115.29.204.48/syl/csi20180212.zip
    day = arrow.get(date, date_format).date()
    weekday = day.weekday()
    # ignore weekend
    if weekday == 5 or weekday == 6:
        return
    url = '{}industry-price-earnings-ratio-detail?date={}&class=2&search=1&csrc_code={}'.format(csi_domain, date, code)
    page = parse(url).getroot()
    # result = etree.tostring(page)
    # print(result)
    xpath = '//table[@class="table table-bg p_table table-border "]'
    r = page.xpath(xpath)
    # print(len(r))
    tree = etree.ElementTree(r[0])
    # print(etree.tostring(tree))
    html_table = etree.tostring(tree)
    dfs = pd.read_html(html_table, flavor='lxml')
    df = dfs[0]
    print(df)
    for index, row in df.iterrows():
        # 个股数据
        code = str(row[1])
        name = row[2]
        code1 = str(row[3])
        code2 = str(row[5])
        code3 = str(row[7])
        code4 = str(row[9])
        row11 = row[11]
        row12 = row[12]
        row13 = row[13]
        row14 = row[14]
        try:
            pe = float(row11)
        except:
            pe = 0

        try:
            pe_ttm = float(row12)
        except:
            pe_ttm = 0

        try:
            pb = float(row13)
        except:
            pb = 0

        try:
            dyr = float(row14)
        except:
            dyr = 0
        print(pe, pe_ttm, pb, dyr)
        Equity.objects(name=name, date=day).update_one(code=code, date=day, name=name,
                                                       code1=code1, code2=code2, code3=code3,
                                                       code4=code4,
                                                       pe=pe, pe_ttm=pe_ttm, pb=pb,
                                                       dividend_yield_ratio=dyr, upsert=True)


def read_equity(code='600276', begin_date='2017-12-28', end_date=None):
    if end_date is None:
        end_date = arrow.now().format(date_format)
    begin_arrow = arrow.get(begin_date, date_format)
    begin = begin_arrow.date()
    end = arrow.get(end_date, date_format).date()
    delta = end-begin
    for i in range(delta.days):
        day = begin_arrow.shift(days=i).format(date_format)
        read_equity_by_date(day, code)