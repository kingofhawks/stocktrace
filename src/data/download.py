'''
Created on 2012-9-19

@author: Simon
'''
#import logging
from util import settings
from util import slf4p


#download all history data
#default will download all history data incrementally
def download(clear='False',stockList='stock_list_all'):
    from parse.yahooparser import downloadHistoryData
    from dao.stockdao import clear,findAllExistentTickers
    from parse.sseparser import downloadQuoteList
    from parse.reutersparser import downloadKeyStatDatas
    from parse.sinaparser import downloadLatestData
    
    #logger = logging.getLogger(__name__)
    logger = slf4p.getLogger(__name__)
    logger.info('***Start download finance data****')
    
    if clear:
        clear();
    #download securities list from sse
    downloadQuoteList(True,False,stockList)
    
    #download statistics from reuters        
    if settings.DOWNLOAD_KEY_STAT:
        downloadKeyStatDatas()
        
    quotes = findAllExistentTickers()
    #download history data from yahoo
    downloadHistoryData(quotes)
    
    #update latest price from yahoo or sina
    #Seems YQL API is not stable,tables often to be locked
    if settings.DOWNLOAD_LATEST_PRICE:
        downloadLatestData(quotes,settings.YAHOO)
    
    logger.info('***Finish download finance data****')