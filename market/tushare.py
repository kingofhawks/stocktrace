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
    for index, value in sorted(data.items()):
        code = value['code']
        roe = value['roe']
        Equity.objects(code=code, date=date).update_one(code=code, date=date, roe=roe, upsert=True)

