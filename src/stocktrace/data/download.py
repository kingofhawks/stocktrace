'''
Created on 2012-9-19

@author: Simon
'''
#import logging
from stocktrace.util import settings
from stocktrace.dao.stockdao import clear,findAllExistentTickers
from stocktrace.stock import Stock,download_stock
from stocktrace.util import slf4p
from stocktrace.parse.sseparser import downloadQuoteList

import redis

logger = slf4p.getLogger(__name__)
# redclient = redis.StrictRedis(host= settings.REDIS_SERVER, port=6379, db=0)


def download2(clearAll= False,downloadLatest = False,downloadHistory = False,parse_industry = False,stockList='stock_list_all'):
    logger.info( 'Begin Download stock list data {}'.format(stockList))
    if clearAll:
        #clear redis cache
        # redclient.flushall()
        clear();

    #download securities list from local
    downloadQuoteList(True,False,stockList)
    quotes = findAllExistentTickers()

    import multiprocessing as mp
    pool = mp.Pool(len(quotes))

    for code in quotes:
        s = Stock(code)
        pool.apply_async(download_stock, args = [s,])

    pool.close()
    pool.join()
    logger.info( '****Download latest price from sina finished****')

#download all history data
#default will download all history data incrementally
def download(clearAll= False,downloadLatest = False,downloadHistory = False,parse_industry = False,stockList='stock_list_all'):
    from stocktrace.parse.yahooparser import downloadHistoryData
    from stocktrace.dao.stockdao import clear,findAllExistentTickers
    from stocktrace.parse.reutersparser import downloadKeyStatDatas
    from stocktrace.parse.sinaparser import downloadLatestData
    from stocktrace.parse.ifengparser import parseIndustry
    from stocktrace.redis.redisservice import findStocksByList
    
    logger.info('***Start download finance data****')
    
    if clearAll:
        #clear redis cache
        # redclient.flushall()
        clear();
    #download industry info from ifeng
    if parse_industry:
        parseIndustry()
    
    #download securities list from local
    downloadQuoteList(True,False,stockList)
    
    #load stock list to redis zset
    loadStockListToRedis(stockList)
    
    #download statistics from reuters        
    if settings.DOWNLOAD_KEY_STAT:
        downloadKeyStatDatas()
        
    quotes = findAllExistentTickers()
    #find from redis cache
    # quotes = findStocksByList(stockList)
    # quotes = stockList
    logger.debug(quotes)
    #update latest price from yahoo or sina
    #Seems YQL API is not stable,tables often to be locked
    if downloadLatest:
        downloadLatestData(quotes,engine = settings.SINA)
        
    if downloadHistory:
        #download history data from yahoo
        downloadHistoryData(quotes,engine = settings.CSV_ENGINE)
    
    logger.info('***Finish download finance data****')

def loadStockListToRedis(stockList):
    import os,io
    fn = os.path.join(os.path.dirname(__file__),'..', '..','resources',stockList)    
    
    with io.open(os.path.abspath(fn),'rb') as f:        
        for i in range(settings.PAGING_TOTAL):
            line = f.readline()
            if (len(line) == 0):
                break;
            else :
                l = line.strip();
                if (len(l)==7):
                    code = l[1:]                    
                    #print len(l)  
                    #print l  
                elif (len(l) == 6):
                    code = l;                   
                else :
                    logger.debug(l);
                    continue
                
                # redclient.zadd(stockList,1.1,code)
    pass
