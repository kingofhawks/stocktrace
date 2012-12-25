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

def filterStocksByIndustry(stocks,industry):
    if (industry is None or industry.find('all')!= -1):
        return stocks
    result = []
    stocksInRedis = redclient.lrange(industry,0,-1)
    if (len(stocksInRedis) == 0):
        return stocks
    for stock in stocks:
        if any(stock.code in s for s in stocksInRedis):
            logger.debug(str(stock.code)+' in '+industry)
            result.append(stock)
    return result

def filterStocksByList(stocks,stockList):
    if (stockList is None):
        return stocks
    result = []
    stocksInRedis = redclient.zrange(stockList,0,-1)
    if (len(stocksInRedis) == 0):
        return stocks
    for stock in stocks:
        if any(stock.code in s for s in stocksInRedis):
            logger.debug(str(stock.code)+' in '+stockList)
            result.append(stock)
    return result

def filterStocksByList2(stocks,stockList):
    if (stockList is None):
        return stocks
    result = []
    stocksInRedis = redclient.zrange(stockList,0,-1)
    if (len(stocksInRedis) == 0):
        return stocks
    for stock in stocks:
        if any(stock in s for s in stocksInRedis):
            logger.debug(str(stock)+'already in '+stockList)
            continue
        else:
            result.append(stock)
    return result

def findStocksByList(stockList):
    stocksInRedis = redclient.zrange(stockList,0,-1)
    return stocksInRedis
        
if __name__ == '__main__':
    stocks = []
    from stocktrace.stock import Stock
    stocks.append(Stock('600327'))
    stocks.append(Stock('601111'))
    stocks.append(Stock('600221'))
    result = filterStocksByIndustry(stocks,'航空运输业')
    for stock in result:
        print stock
    
    
        
    