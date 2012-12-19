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
    result = []
    stocksInRedis = redclient.lrange(industry,0,-1)
    for stock in stocks:
        if any(stock in s for s in stocksInRedis):
            logger.debug(stock+' in '+industry)
            result.append(stock)
    return result
        
if __name__ == '__main__':
    stocks = ['600327','600371','600583']
    print(filterStocks(stocks,'农、林、牧、渔业'))
    
    
        
    