import tushare as ts

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
