#!/usr/bin/env python

import thread,logging
from stocktrace.dao.stockdao import findAllExistentTickers
from stocktrace.stock import Stock
from stocktrace.util import slf4p

logger = slf4p.getLogger(__name__)

#quote state cache
stateCache = {}

def getStock(code):
    #Sina API
    if (code.startswith('60')):
        code = 'sh'+code
    else:
        code = 'sz'+code
    url = "http://hq.sinajs.cn/list="+code
    logger.debug(url)
    #Google Finance API
    #url = 'http://finance.google.com/finance/info?q=600030'    
    import urllib2,os,sys    

    pg = urllib2.urlopen(url)
    cont = pg.read()
    #print cont
    test = cont.split(',')
    if (len(test) <9):
        logger.error('error passe:'+code)
        return 
    yesterday = float(test[2])
    current = float(test[3])
    high = float(test[4])
    low = float(test[5])
    volume = float(test[8])
    percent = (current-yesterday)/yesterday*100
    name = test[0].split('"')[1]
    logger.debug(name)
    # logger.debug(str(name))
    enc = "gbk"
    u_content = name.decode(enc) # decodes from enc to unicode
    utf8_name = u_content.encode("utf8")
    logger.debug(utf8_name)
    stock = Stock(code,current,percent,low,high,volume)
    stock.name = utf8_name
    
    #check threshold
    if (current == 0.0):
        pass
    elif (percent >=2):
        #Alarm
        stock.alert = True;        
        stock.state = 'UP'
    elif (percent <=-5):
        #Alarm
        stock.alert = True;        
        stock.state = 'CRITICAL'
    elif (percent <=-2):
        #Alarm
        stock.alert = True;        
        stock.state = 'WARNING'
    elif (stock.code == 'sh000001' and (percent >=1 or percent <=-1)):
        stock.state = 'WARNING'
        
    #check whether state changed
    state = stateCache.get(code)
    #print state
    
    if (state!= stock.state):
        stateCache[code] = stock.state;
        pass
    else:
        stock.alert = False;

    logger.info( '****Download latest price from SINA finished****'+stock.code)
    logger.info(stock)
    return stock
    
    #print '%.2f'%percent+'%'   
    #print sys.argv[0]    
    
def getMyStock(codes = ['sh600327','sh600600','sh601111','sh600221','sh600583','sh600573','sh600428','sh000001']):
    stocksCrossThreshold = [] 
    for code in codes: 
        stock = getStock(code)
        logger.debug(stock.shortStr())
        if (stock.alert == True):
            stocksCrossThreshold.append(stock.shortStr())
        #thread.start_new(getStock,(code,))
    
    if (len(stocksCrossThreshold) !=0):
        from stocktrace.util.mailutil import sendMail
        print stocksCrossThreshold
        message = str(stocksCrossThreshold)
        #sendMail(message)
        #publish message to rabbitmq
        import pika
        import sys
        from stocktrace.util import settings
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=settings.RABBIT_SERVER))
        channel = connection.channel()        
        
        channel.exchange_declare(exchange= settings.STOCK_ALARMS_TOPIC,
                                 type='topic')
        
        routing_key = 'stock_trigger_threshold'
        #message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(exchange=settings.STOCK_ALARMS_TOPIC,
                              routing_key=routing_key,
                              body=message)
        print " [x] Sent %r:%r" % (routing_key, message)
        connection.close()
    
    print '******************finished quote polling***********************'

#download latest price info from sina
def downloadLatestData(quotes = findAllExistentTickers(),engine='sina'):
    logger.info( '****Begin Download latest price from SINA****'+str(len(quotes)))
    import multiprocessing as mp
    pool = mp.Pool(len(quotes))
    
    for code in quotes: 
        update(code,engine)
        pool.apply_async(update, args = [str(code),engine])
    
    pool.close()
    pool.join()        
    logger.info( '****Download latest price from sina finished****')
        

def update(code,engine='sina'):
    if engine == 'sina':
            quote = getStock(code)
    elif engine == 'yahoo':
            from stocktrace.parse.yahooparser import parseFinanceData
            quote = parseFinanceData(code)            
    if (code.startswith('sh')):
            code = code.replace('sh','')

    logger.debug(quote)
    if quote is not None:
            from stocktrace.dao.stockdao import updateTickerToLatestPrice
            # updateTickerToLatestPrice(code,quote.close,quote.ma50,quote.ma200,quote.yearHigh,quote.yearLow,quote.PercentChangeFromYearHigh,quote.PercentChangeFromYearLow,quote.name)
            updateTickerToLatestPrice(code,quote.current,quote.ma50,quote.ma200,quote.yearHigh,quote.yearLow,quote.PercentChangeFromYearHigh,quote.PercentChangeFromYearLow,quote.name)
            
if __name__ =="__main__":    
    import time, os, sys, sched
#    schedule = sched.scheduler(time.time, time.sleep)
#    schedule.enter(0, 0, getMyStock, ())   # 0==right now
#    schedule.run( )
    #getMyStock()    
    #downloadLatestData();
#    import urllib2
#    h=urllib2.HTTPHandler(debuglevel=1)    
#    request = urllib2.Request('http://finance.google.com/finance/info?q=600030')
#    request.add_header('User-Agent','StockTrace/1.0') 
#    opener = urllib2.build_opener(h) 
    #feeddata = opener.open(request).read()  
    #print feeddata
    #print os.path.abspath(os.path.dirname(sys.argv[0]))
    #print sys.argv[0]
    
