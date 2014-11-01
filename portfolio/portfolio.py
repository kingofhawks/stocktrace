from dao import find_all_stocks,update_stock_price,insert_stock,add_tag
from stocktrace.parse.sinaparser import getStock
from stocktrace.stock import Stock


def polling():
    stocks = find_all_stocks()
    for stock in stocks:
        code = stock['code']
        s = getStock(code)
        print s
        try:
            update_stock_price(code,s.current)
        except AttributeError:
            continue
    return stocks


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
        print code
        add_tag(code,portfolio)
        # stock = Stock(code)
        # insert_stock(stock)


def snapshot(save=True):
    stocks = polling()
    from models import Portfolio
    portfolio = Portfolio(stocks)
    if save:
        portfolio.save()
    return portfolio


if __name__=='__main__':
    polling()
