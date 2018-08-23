import tushare as ts

from market.models import Equity
from stocktrace.stock import Stock


def stock_list():
    df = ts.get_stock_basics()
    data = df.to_dict('index')
    for code, value in sorted(data.items()):
        # print(code)
        # print(value['name'])
        Stock.objects(code=code).update_one(code=code, name=value['name'], upsert=True)
    # print(data)
    # stocks = df.index.tolist()
    # print(stocks)


def profit():
    df = ts.get_profit_data(2018, 2)
    print(df)
    data = df.to_dict('index')
    print(data)
    for code, value in sorted(data.items()):
        # print(value)
        if value['code'] == '600420':
            print(value)


def finance_report(year=2018, quarter=2):
    latest_equity = Equity.objects().order_by('-date').first()
    # print(latest_equity)
    date = latest_equity.date

    df = ts.get_report_data(year, quarter)
    print(df)
    data = df.to_dict('index')
    print(data)
    from mongoengine.queryset.visitor import Q
    for index, value in sorted(data.items()):
        code = value['code']
        roe = value['roe']
        # Equity.objects(code=code).update(code=code, roe=roe, upsert=True)
        # Equity.objects(__raw__={"code":code,"date" : {"$gte":'2018-07-01',"$lte":'2018-08-31'}}).update(code=code, roe=roe, upsert=True)
        # 只更新最近一个季度的数据
        Equity.objects(Q(code=code) & Q(date__gte='2018-07-01') & Q(date__lte='2018-08-31')).update(roe=roe)
