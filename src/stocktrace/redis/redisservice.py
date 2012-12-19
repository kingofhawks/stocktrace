#-*- coding: UTF-8 -*-

'''
Created on 2012-12-19

@author: Simon
'''
import redis
from stocktrace.util import slf4p
from stocktrace.util import settings

logger = slf4p.getLogger(__name__)
redclient = redis.StrictRedis(host=settings.REDIS_SERVER, port=6379, db=0)

def filterStocks(stocks,industry):
    if (industry is None or industry.find('all')!= -1):
        return stocks
    result = []
    stocksInRedis = redclient.lrange(industry,0,-1)
    for stock in stocks:
        if any(stock.code in s for s in stocksInRedis):
            logger.debug(str(stock.code)+' in '+industry)
            result.append(stock)
    return result
        
if __name__ == '__main__':
    stocks = []
    from stocktrace.stock import Stock
    stocks.append(Stock('600327'))
    stocks.append(Stock('601111'))
    stocks.append(Stock('600221'))
    result = filterStocks(stocks,'航空运输业')
    for stock in result:
        print stock
    
    
        
    