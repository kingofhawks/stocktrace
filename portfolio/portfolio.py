from market.utils import get_date
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


def snapshot():
    stocks = polling()
    print(stocks)
    stock_list = []
    for stock in stocks:
        stock_list.append({'code': stock['code'], 'name': stock['name'],
                           'amount': stock['amount'],
                           'current': stock['current'], 'percentage': stock['percentage'],
                           'change': stock['change'] or 0})

    from portfolio.models import Portfolio
    from datetime import date
    date = get_date(str(date.today()))
    print('date***{}'.format(date))
    p = Portfolio(list=stock_list)
    p.compute()
    Portfolio.objects(date=date).update_one(list=p.list, market_value=p.market_value, total=p.total,
                                            net_asset=p.net_asset, cost=p.cost, cost_history=p.cost_history,
                                            cost_zs=p.cost_zs, cost_ht1=p.cost_ht1, cost_ht2=p.cost_ht2,
                                            cost_ht1_real=p.cost_ht1_real, cost_ht2_real=p.cost_ht2_real,
                                            position_ratio=p.position_ratio, financing=p.financing,
                                            lever=p.lever, cash=p.cash, profit=p.profit,
                                            profit_ratio=p.profit_ratio, profit_today=p.profit_today,
                                            profit_ratio_today=p.profit_ratio_today,
                                            upsert=True)
    result = Portfolio.objects.get(date=date)
    if result:
        print('result list***{}'.format(result.list))
        return result
    else:
        return None


if __name__ == '__main__':
    polling()
