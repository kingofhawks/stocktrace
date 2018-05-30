from portfolio.dao import find_all_stocks, update_stock_price, insert_stock, add_tag, find_stock_by_code
from market.parse import sina, xueqiu, polling
from stocktrace.stock import Stock
import traceback


# get real-time market value
def market_value(stocks):
    total = 0
    for stock in stocks:
        code = stock['code']
        # s = getStock(code)
        # # print 'current:{} amount:{}'.format(s.current, stock['amount'])
        # total += float(s.current) * float(stock['amount'])
    return total


def import_portfolio(file,portfolio):
    p = []
    content = ''
    with open(file) as f:
        #read file to list line by line
        # p = f.readlines()
        #read whole file
        content = f.read()
    #this will remove the newline character
    p = content.splitlines()
    # logger.debug('content:{}'.format(content))
    # logger.debug(p)
    for line in p:
        code = line[1:]
        #logger.debug(code)
        # print code
        add_tag(code,portfolio)
        # stock = Stock(code)
        # insert_stock(stock)


def snapshot(save=True):
    stocks = polling()
    print(stocks)
    from portfolio.models import Portfolio
    from datetime import date
    from django.conf import settings
    db = settings.DB
    name = str(date.today())
    portfolios = db.portfolio
    portfolio = portfolios.find_one({"name": name})
    if portfolio:
        stock_list = []
        for stock in stocks:
            stock_list.append({'code': stock['code'], 'amount': stock['amount'], 'current': stock['current']})
        portfolios.update({"name": name}, {"$set": {"stocks": stock_list}}, upsert=True)
        portfolio['stocks'] = stocks
    else:
        portfolio = Portfolio(stocks)
        portfolio.save()
    result = Portfolio(stocks)
    return result


if __name__ == '__main__':
    polling()
