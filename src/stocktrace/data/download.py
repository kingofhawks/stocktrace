'''
Created on 2012-9-19

@author: Simon
'''
#import logging
from stocktrace.util import settings
from stocktrace.util import slf4p
import redis

logger = slf4p.getLogger(__name__)
redclient = redis.StrictRedis(host='172.25.21.16', port=6379, db=0)

#download all history data
#default will download all history data incrementally
def download(clearAll= False,downloadLatest = False,downloadHistory = False,stockList='stock_list_all'):
    from stocktrace.parse.yahooparser import downloadHistoryData
    from stocktrace.dao.stockdao import clear,findAllExistentTickers
    from stocktrace.parse.sseparser import downloadQuoteList
    from stocktrace.parse.reutersparser import downloadKeyStatDatas
    from stocktrace.parse.sinaparser import downloadLatestData
    
    logger.info('***Start download finance data****')
    
    if clearAll:
        #clear redis cache
        redclient.flushall()
        clear();
    #download securities list from sse
    downloadQuoteList(True,False,stockList)
    
    #download statistics from reuters        
    if settings.DOWNLOAD_KEY_STAT:
        downloadKeyStatDatas()
        
    quotes = findAllExistentTickers()
    
    #update latest price from yahoo or sina
    #Seems YQL API is not stable,tables often to be locked
    if downloadLatest:
        downloadLatestData(quotes,settings.YAHOO)
        
    if downloadHistory:
        #download history data from yahoo
        downloadHistoryData(quotes,engine = settings.YAHOO)
    
    logger.info('***Finish download finance data****')