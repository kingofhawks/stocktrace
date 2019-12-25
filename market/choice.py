import pandas as pd
from market.models import Index
import numpy as np
import math

code = {'000015.SH': '红利指数', '000016.SH': '上证50', '000300.SH': '沪深300',
        '000905.SH': '中证500', '000903.SH': '中证100', '000906.SH': '中证800',
        '399005.SZ': '中小板', '399006.SZ': '创业板', '399102.SZ': '创业板综',
        '000918.SH': '300成长', '000919.SH': '300价值', '000821.SH': '300红利',
        '000913.SH': '300医药', '399986.SZ': '中证银行', '399995.SZ': '基建工程',
        '000922.SH': '中证红利',
        '000925.SH': '基本面50', '000932.SH': '中证消费',
        '000934.SH': '中证金融', '000018.SH': '180金融',
        'HSI.HI': '恒生指数',
        'DJIA.GI': '道琼斯工业',  'IXIC.GI': '纳斯达克', 'SPX.GI': '标普500'}


def index_stats(file):
    file_name = 'D:\workspace\stocktrace\data\{}.xls'.format(file)
    # set sheet_name to None will read all sheets to map of DF
    # index_col 2 will read the 2nd column as index(时间列)
    #  '--' is recognized as None
    # parse_dates will auto-parse datetime
    sheet_to_df_map = pd.read_excel(file_name, sheet_name=None, index_col=2, na_values=['--'], parse_dates=True)
    for sheet in sheet_to_df_map:
        df = sheet_to_df_map[sheet]
        # print(df)
        # 过滤掉PE(TTM)列为空的行
        df = df.dropna(subset=['PE(TTM)'])
        # print(df.columns)
        # print(df.index)
        # 取最近5年数据
        # df = df.last('1825D')
        # df = df.last('5Y')
        # print(df.tail(1))
        # get the last row as pandas.Series which is easier to get row value
        last_pe = df.iloc[-1]['PE(TTM)']
        # print(last_pe)
        # print(df)
        # a = np.array(df['PE(TTM)'])
        # print(a)
        # median1 = np.percentile(a, 0.5)
        # median1 = np.median(a)
        max_pe = df['PE(TTM)'].max()
        min_pe = df['PE(TTM)'].min()
        mean = df['PE(TTM)'].mean()
        median = df['PE(TTM)'].median()
        # 30分位
        p30 = df['PE(TTM)'].quantile(0.3)
        # 70分位
        p70 = df['PE(TTM)'].quantile(0.7)
        # a = [max_pe, min_pe, mean, median, p30, p70]
        # np.percentile 类似于pandas.quantile
        # percent = np.percentile(a, last_pe)
        # 保留两位小数输出
        print('{} PE max:{:.2f} min:{:.2f} mean:{:.2f} median:{:.2f} 30分位%:{:.2f} 70分位%:{:.2f} '
              'current:{:.2f} 红绿灯:{}'
              .format(code.get(sheet), max_pe, min_pe, mean, median, p30, p70, last_pe, last_pe < p30 ))


@DeprecationWarning
def index_stats_2(code):
    file_name = 'D:\workspace\stocktrace\market\{}.xls'.format(code)
    # footer_len = get_footer(file_name)
    skiprows = range(3000, 3500)
    df = pd.read_excel(file_name)
    # 过滤掉PE(TTM)列为空的行
    df = df[df['PE(TTM)'] != '--']
    print(df)
    print(len(df))
    max_pe = df['PE(TTM)'].max()
    min_pe = df['PE(TTM)'].min()
    mean = df['PE(TTM)'].mean()
    median = df['PE(TTM)'].median()
    print(max_pe)
    print(min_pe)
    print(mean)
    print(median)
    data = df.to_dict('index')
    # print(data)
    # print(len(data.items()))
    for index, value in sorted(data.items()):
        print(value)
        code = value['代码']
        name = value['简称']
        date = value['时间']
        pe_ttm = value['PE(TTM)']
        pb = value['市净率PB(MRQ)']
        volume = value['成交金额(元)']
        float_market = value['流通市值(元)']
        turnover = volume/float_market
        if date and pe_ttm and pb and turnover:
            Index.objects(name=name, date=date).update_one(name=name, code=code,date=date, pe=pe_ttm, pe_ttm=pe_ttm,
                                                           volume=volume, pb=pb,
                                                           turnover=turnover,
                                                           upsert=True)


if __name__ == '__main__':
    # 10年10倍求年化收益率为25.89%,使用开方运算
    print(10**(1/10))
    a = [40.7, 20.52, 28.12, 27.66, 25.89, 29.85]
    # 求数组中50分位的数值
    print(np.percentile(a, 50))
    # index_stats('choice20191122_core')
    # index_stats('choice20191122_zz')
    index_stats('choice20191122_other')
    # index_stats_2('000300')