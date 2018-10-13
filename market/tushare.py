import pymongo
import tushare as ts

from market.models import Equity, FinanceReport
from stocktrace.stock import Stock


DB_NAME = 'stocktrace'
DB_HOST = 'localhost'
db = getattr(pymongo.MongoClient(host=DB_HOST), DB_NAME)


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


def ipo():
    ts.set_token('b4c94429dc00fee32d14c52507d9cd44c9621ca91eaa161fcec14041')
    pro = ts.pro_api()

    # 查询当前所有正常上市交易的股票列表
    df = pro.stock_basic(exchange_id='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print(df)
    data = df.to_dict('index')
    print(data.items())
    for item, value in sorted(data.items()):
        code = value['symbol']
        ipo_date = value['list_date']
        Stock.objects(code=code).update_one(code=code, ipo_date=ipo_date, upsert=True)


# 破发率
def broken_ipo(begin='2018-01-01', end='2018-12-31'):
    stocks = db.stock.find({"ipo_date": {"$gte": str(begin), "$lte": str(end)}}).sort([("ipo_date", pymongo.DESCENDING)])
    print(list(stocks))


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
    print(len(data.items()))
    from mongoengine.queryset.visitor import Q
    for index, value in sorted(data.items()):
        code = value['code']
        name = value['name']
        roe = value['roe']
        eps = value['eps']
        report_date = value['report_date']
        # print('code:{} roe:{}'.format(code, roe))
        FinanceReport.objects(code=code, year=year, quarter=quarter).update_one(code=code, name=name,
                                                                                year=year, quarter=quarter,
                                                                                report_date=report_date,
                                                                                roe=roe, eps=eps, upsert=True)
        # Equity.objects(code=code).update(code=code, roe=roe, upsert=True)
        # Equity.objects(__raw__={"code":code,"date" : {"$gte":'2018-07-01',"$lte":'2018-08-31'}}).update(code=code, roe=roe, upsert=True)
        # 只更新最近一个季度的数据
        # Equity.objects(Q(code=code) & Q(date__gte='2018-07-01') & Q(date__lte='2018-08-31')).update(roe=roe)
