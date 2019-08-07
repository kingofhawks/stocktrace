import pandas as pd
from market.models import Index
import numpy as np


def index_stats(file):
    file_name = 'D:\workspace\stocktrace\market\{}.xls'.format(file)
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
        # get last 5 Year data
        # print(df)
        # df = df.last('1825D')
        # print(df)
        # df = df.last('5Y')
        # print(df)
        # a = np.array(df['PE(TTM)'])
        # print(a)
        # median1 = np.percentile(a, 0.5)
        # median1 = np.median(a)
        max_pe = df['PE(TTM)'].max()
        min_pe = df['PE(TTM)'].min()
        mean = df['PE(TTM)'].mean()
        median = df['PE(TTM)'].median()
        p30 = df['PE(TTM)'].quantile(0.3)
        p70 = df['PE(TTM)'].quantile(0.7)
        print('{} PE max:{} min:{} mean:{} median:{} 30%:{} 70%:{}'.format(sheet, max_pe, min_pe, mean, median, p30, p70))



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
    index_stats('choice')
    # index_stats_2('000300')