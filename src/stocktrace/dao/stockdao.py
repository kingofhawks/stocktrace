'''
Created on 2011-3-7

@author: simon
'''
import pymongo
from datetime import date
from datetime import timedelta
from datetime import datetime
from stocktrace.util import slf4p,settings
#from stocktrace.memcache.cache import Cache 
from pymongo import Connection 
#from memorised.decorators import memorise
from stocktrace.stock import Stock
    
connection = Connection()      
#cache = Cache() 
logger = slf4p.getLogger(__name__)
    
def insertStock():
    connection = Connection()
    db = connection.test_database
    collection = db.test_collection
    import datetime
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    posts = db.posts
    posts.insert(post)
    posts.find_one()
    posts.find_one({"author": "Mike"})
    for post in posts.find():
        print post
 
#save stock trading history         
def saveStock(stock):
    #connection = Connection()
    db = connection.stock
    data = {"code": stock.code,
            "high": stock.high,
            "low": stock.low,
            "open": stock.openPrice,
            "close": stock.close,
            "volume": stock.volume,
            "date": stock.date}
    historyDatas = db.stock_history
    historyDatas.insert(data)
    #connection.end_request()
        
def findAllStocks():
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    for stock in historyDatas.find():
        print stock   
        
#find last update stock record        
def findLastUpdate(code):
    print "To find latest update****"+code
    #connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
#    print historyDatas.find_one({"code": code})
    #print historyDatas.find({"code": code}).sort([("date",pymongo.DESCENDING)]).limit(1)
    return historyDatas.find_one({"code": code},sort=[("date",pymongo.DESCENDING)]);

#find the oldest stock record        
def findOldestUpdate(code):
    print "To find oldest update****"+code
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
#    print historyDatas.find_one({"code": code})
    #print historyDatas.find({"code": code}).sort([("date",pymongo.DESCENDING)]).limit(1)
    return historyDatas.find_one({"code": code},sort=[("date",pymongo.ASCENDING)]);
   
#find stock record after date     
def findStockByDate(code,date):
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    return historyDatas.find({"code":code,"date" : {"$gt":date}}).sort([("date",pymongo.DESCENDING)]);

#find quote history data by code     
def findStockByCode(code):
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    return historyDatas.find({"code":code}).sort([("date",pymongo.DESCENDING)]);


def find_week52_history(code):
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    delta = timedelta(-52*7)
    begin = date.today()+delta
    return historyDatas.find({"code":code,"date" : {"$gte":str(begin)}}).sort([("date",pymongo.DESCENDING)]);


def update_week52(code):
    connection = Connection()
    db = connection.stock
    ticker = db.tickers
    import pandas as pd
    result = find_week52_history(code)
    logger.debug(result)
    df = pd.DataFrame(list(result))
    logger.debug(df)
    logger.debug(df.shape)
    logger.debug(df['low'].min())
    logger.debug(df['low'].argmin())
    logger.debug(df['high'].max())
    high_week52_index = df['high'].argmax()
    low_week52_index = df['low'].argmin()
    logger.debug(high_week52_index)
    logger.debug(df[['date','high']][high_week52_index:high_week52_index+1])
    logger.debug(df[['date','low']][low_week52_index:low_week52_index+1])
    # print ticker.update({"code":stock},
    # {"$set":{"yearHigh":df['high'].max(),"yearLow":df['low'].min(),"percentFromYearHigh":percentFromYearHigh,"percentFromYearLow":percentFromYearLow}},
    # upsert=True,safe=True)
    year_high = df['high'].max()
    year_low = df['low'].min()
    last_update = findLastUpdate(code)
    current = last_update['close']
    logger.debug(current)
    percentFromYearHigh = (year_high-current)*100/year_high
    percentFromYearLow = (current-year_low)*100/year_low
    print ticker.update({"code":code},
    {"$set":{"yearHigh":year_high,"yearLow":year_low,"percentFromYearHigh":percentFromYearHigh,"percentFromYearLow":percentFromYearLow}},
    upsert=True,safe=True)



def countByCode(code):
    connection = Connection()
    db = connection.stock
    return db.stock_history.find({"code":code}).count();
    

#find stock record in the last days     
def findLastStockByDays(code,lastDays):
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    from datetime import date
    from datetime import datetime
    from datetime import timedelta
    print date.today()
    delta = timedelta(-lastDays)
    begin = date.today()+delta
    print begin
    #print datetime.strptime(date,'%Y-%m-%d')
    #print type(date.today())    
       
    key = str(code)+'_'+str(lastDays)
    print key
    try:
        #result = cache.get(key)
        result = None
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
    
    if result is not None:
        print 'cache'
        return result
    else:
        result = historyDatas.find({"code":code,"date" : {"$gt":str(begin)}}).sort([("date",pymongo.ASCENDING)]);
#        print result
#        #records = [(record['_id'], record) for record in result]
        cols = []
        for record in result:
            cols.append(record)
        #print cols
        #cache.set(key, cols)
        print 'sql'
        return cols
    
    #return historyDatas.find({"code":code,"date" : {"$gt":str(begin)}}).sort([("date",pymongo.ASCENDING)]);

#find peak price during the last days before endDate
def findPeakStockByDays(code,lastDays,endDate = str(date.today())):
    delta = timedelta(-lastDays)
    end = datetime.strptime(endDate,'%Y-%m-%d').date()
    print end
    begin = end+delta
#    begin = date.today()+delta
    
    print begin
#    print begin.weekday()
    key = str(code)+'_'+str(lastDays)+'_'+endDate+'_high'
    peak = cache.get(key)
    if peak is not None:
        print 'cache'
        return peak
    else:
        connection = Connection()
        db = connection.stock
        historyDatas = db.stock_history
        peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("high",pymongo.DESCENDING)]).limit(1);
        try:
            print code+' peak price****'+str(peak[0])
            cache.set(key,peak[0])
            return peak[0]
        except:
            logger.error('Fail to find peak price:'+code)
            return None
    #peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("high",pymongo.DESCENDING)]).limit(1);

    

#find bottom price during the last days 
def findBottomStockByDays(code,lastDays,endDate = str(date.today())):
#    from pymongo import Connection
#    connection = Connection()
#    db = connection.stock
#    historyDatas = db.stock_history
#    delta = timedelta(-lastDays)
#    end = datetime.strptime(endDate,'%Y-%m-%d').date()
#    begin = end+delta
#    key = str(code)+'_'+str(lastDays)+'_'+endDate+'_low'
#    print key
#    peak = cache.get(key)
#    if peak is not None:
#        print 'cache'
#        return peak
#    else:        
#        peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("low",pymongo.ASCENDING)]).limit(1);
#        print code+' low price****'+str(peak[0])
#        cache.set(key,peak[0])
#        return peak[0]
     return findHighOrLowStockByDays(code,lastDays,2)
    
def findHighOrLowStockByDays(code,lastDays,mode=1,endDate = str(date.today())):    
    delta = timedelta(-lastDays)
    end = datetime.strptime(endDate,'%Y-%m-%d').date()
    print end
    begin = end+delta
#    begin = date.today()+delta
    
    print begin
#    print begin.weekday()
    key = str(code)+'_'+str(lastDays)+'_'+endDate+'_high'
    if mode == 2:
        key = str(code)+'_'+str(lastDays)+'_'+endDate+'_low'
    peak = cache.get(key)
    if peak is not None:
        print 'cache'
        return peak
    else:
        connection = Connection()
        db = connection.stock
        historyDatas = db.stock_history
        if mode == 1:
            peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("high",pymongo.DESCENDING)]).limit(1);
        else:
            peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("low",pymongo.ASCENDING)]).limit(1);
        try:
            print code+' peak price****'+str(peak[0])
            cache.set(key,peak[0])
            return peak[0]
        except:
            logger.error('Fail to find peak price:'+code)
            return None
    #peak = historyDatas.find({"code":code,"date" : {"$gte":str(begin),"$lte":str(end)}}).sort([("high",pymongo.DESCENDING)]).limit(1);
        
#Check whether the stock triggers NH-NL index
#lastDays: the last range to check the index
#newDays: the latest days trigger the index
#return 1 as trigger NH index,-1 as trigger NL index,0 as none
def triggerNhNl(code,lastDays=200,nearDays=5,endDate = str(date.today())):
    #find peak price during the last days
    #count = countByCode(code)
    #ignore too less data <=1 month
#    if count <= 20:
#        return 0;
    peak = findPeakStockByDays(code,lastDays,endDate)
    print code+str(peak)
    
    if peak is None:
        return 0;
    
    #check peak price whether happen during near days
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d')
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d').date()
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d').date()<date.today()
    delta = timedelta(-nearDays)
    end = datetime.strptime(endDate,'%Y-%m-%d').date()
    begin = end+delta
#    print begin
    result = datetime.strptime(peak.get('date'),'%Y-%m-%d').date()>=begin
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d').date()<=date.today()
    if result:
        print code+' trigger NH index at '+str(peak)
        return {'date':peak.get('date'),'value':1};
    
    
    #find bottom price during the last days
    bottom = findBottomStockByDays(code,lastDays,endDate)
    print bottom
    if bottom is None:
        return 0;
    #check bottom price whether happen during near days
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d')
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d').date()
#    print datetime.strptime(peak.get('date'),'%Y-%m-%d').date()<date.today()
#    delta = timedelta(-nearDays)
#    begin = date.today()+delta
#    print begin
    result = datetime.strptime(bottom.get('date'),'%Y-%m-%d').date()>=begin
    print datetime.strptime(bottom.get('date'),'%Y-%m-%d').date()<=end
    if result:
        print code+' trigger NL index at '+str(bottom)
        #return -1;
        return {'date':bottom.get('date'),'value':-1};
    return 0

#save ticker with code and year high/low etc
def saveTicker(stock):
    connection = Connection()
    db = connection.stock
    data = {"code": stock.code,
            "name": stock.name,
            "high": stock.high,
            "low": stock.low,
            "yearhigh": stock.yearHigh,
            "yearlow": stock.yearLow,
            "close": stock.close}
    historyDatas = db.tickers
    historyDatas.insert(data)

#batch save ticker with code
def batchInsertTicker(stocks):
    connection = Connection()
    db = connection.stock
    datas = []
    for stock in stocks:
        datas.append({"code": stock})
    historyDatas = db.tickers
    historyDatas.insert(datas)
    
#Update ticker with key statistics data
def updateTickerWithKeyStats(stock,eps,bookingValue,marketCap = 0):
    connection = Connection()
    db = connection.stock
    ticker = db.tickers
    print ticker.update({"code":stock},
    {"$set":{"mgsy":float(eps), "mgjzc":float(bookingValue)}}, upsert=True,safe=True)
     #,"marketCap":marketCap}
    
#Update ticker with latest price
def updateTickerToLatestPrice(stock,current,ma50=0.0,ma200=0.0,yearHigh=0.0,yearLow=0.0,percentFromYearHigh=0.0,percentFromYearLow=0.0,name = ''):
    connection = Connection()
    db = connection.stock
    ticker = db.tickers
    logger.info('current:'+str(current))
    logger.info(ticker.update({"code":stock},
    {"$set":{"current":current,"ma50":ma50,"ma200":ma200,"yearHigh":yearHigh,"yearLow":yearLow,
             "percentFromYearHigh":percentFromYearHigh,"percentFromYearLow":percentFromYearLow,"name":name}},
    upsert=True,safe=True))
    
#save non-existent tickers,may change according to IPO
def saveNonExistentTicker(stock):
    connection = Connection()
    db = connection.stock
    data = {"code": stock.code}
    historyDatas = db.non_existent_tickers
    historyDatas.insert(data)
    
def findAllNonExistentTickers():
    connection = Connection()
    db = connection.stock
    historyDatas = db.non_existent_tickers
    cursor = historyDatas.find();
    from sets import Set
    result = Set([])
    for stock in cursor:
        result.add(stock['code'])
    return result

def findAllExistentTickers():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    cursor = historyDatas.find();
    from sets import Set
    result = Set([])
    for stock in cursor:
        result.add(stock['code'])
    return result

#find all quotes list
def findAllQuotes():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    cursor = historyDatas.find();
    result = []
    for stock in cursor:
        result.append(stock['code'])
    return result


#Define market PE as mid PE of all stocks
def getMarketPe():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    all = historyDatas.find().sort([("pe",pymongo.DESCENDING)]);
    mid = all.count()/2
    #print mid
    midPe = all[mid]['pe']
    return midPe

#Define market PB as mid PB of all stocks
def getMarketPb():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    all = historyDatas.find().sort([("pb",pymongo.DESCENDING)]);
    mid = all.count()/2
    #print mid
    midPb = all[mid]['pb']
    return midPb

#Define average PE as mid PE of all stocks
def getAvgPe():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    allQuotes = historyDatas.find();
    peList = []
    for stock in allQuotes:
        #print stock
        if (stock.get('close') is None or stock.get('mgsy') is None ):
            continue
        elif (stock['mgsy'] == 0):
            continue
        pe = stock['close']/stock['mgsy']
        #print pe
        peList.append(pe)
        #result.add(stock['code'])
    peList.sort()
    mid = len(peList)/2
    print mid
    midPe = peList[mid]
    return midPe

#Define average PB as mid PB of all stocks
def getAvgPb():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    allQuotes = historyDatas.find();
    pbList = []
    for stock in allQuotes:
        #print stock
        if (stock.get('close') is None or stock.get('mgjzc') is None ):
            continue
        pb = stock['close']/stock['mgjzc']
        #print pb
        pbList.append(pb)
        #result.add(stock['code'])
    pbList.sort()
    mid = len(pbList)/2
    return pbList[mid]

#get those PB<=1
def getPbLessThan1():
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    allQuotes = historyDatas.find();
    pbList = []
    for stock in allQuotes:
        #print stock
        if (stock.get('close') is None or stock.get('mgjzc') is None ):
            continue
        pb = stock['close']/stock['mgjzc']
        #print pb
        if (pb <1):
            pbList.append({'code':stock['code'],'pb':pb})
        #result.add(stock['code'])
    pbList.sort()
    return pbList

#clear all data in system
def clear():
    connection = Connection()
    db = connection.stock
    db.tickers.remove()
    db.non_existent_tickers.remove()
    db.stock_history.remove()
    logger.info('********All history finance data cleared***********')
    pass

#return True if always higher or lower than MA during last days
def checkStockWithMA(code,lastDays=10,ma=10,condition=settings.HIGHER):
    result = True;
    
    stocks = findLastStockByDays(code, (lastDays+ma)*7/5);
    
    ohlc = []
    
    for stock in stocks:
      #print stock
      #open/high/low/close must be float value
      s = []
      s.append(stock['date'])
      s.append(float(stock['open']))
      s.append(float(stock['high']))
      s.append(float(stock['low']))
      s.append(float(stock['close']))
      #print s
      ohlc.append(s)
      
    size = len(ohlc)
    #print ohlc  
    if size == 0:
        logger.error('No data found****'+code)
        return False
    
    #Compute MA
    for i in range(ma,size):
        close = ohlc[i][4]
        maSum = 0.0;
               
        for j in range(i-ma+1,i+1):
            maSum = maSum +ohlc[j][4]
        temp = maSum/ma
        
        if condition == settings.HIGHER and close < temp:
            return False
        elif condition == settings.LOWER and close > temp:
            return False            
       
    
    #print ma1
     
    return result  

#return MA data during last days
def getMa(code,lastDays=10,ma=10):
    result = [];
    
    stocks = findLastStockByDays(code, (lastDays+ma)*7/5);
    
    ohlc = []
    
    for stock in stocks:
      #print stock
      #open/high/low/close must be float value
      s = []
      s.append(stock['date'])
      s.append(float(stock['open']))
      s.append(float(stock['high']))
      s.append(float(stock['low']))
      s.append(float(stock['close']))
      #print s
      ohlc.append(s)
      
    size = len(ohlc)
    #print ohlc  
    if size == 0:
        logger.error('No data found****'+code)
        return result    
    
    #Compute MA
    for i in range(ma,size):
        close = ohlc[i][4]
        maSum = 0.0;
               
        for j in range(i-ma+1,i+1):
            maSum = maSum +ohlc[j][4]
        temp = maSum/ma
        
        result.append(temp)           
       
    
    #print ma1
     
    return result   
    
def findStockByGroup():
    connection = Connection()
    db = connection.stock
    historyDatas = db.stock_history
    return historyDatas.group(['code'], None,
                        {'list': []}, # initial
                        'function(obj, prev) {prev.list.push(obj)}') 
    
#find top N quotes by Price Volatility from yearLow 
#@memorise(cache.getmc())    
def findByYearLow(top=20):
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    return historyDatas.find().sort([("percentFromYearLow",pymongo.DESCENDING)]).limit(top);

#find top N quotes by Price Volatility from yearHigh     
def findByYearHigh(top=20):
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    return historyDatas.find().sort([("percentFromYearHigh",pymongo.DESCENDING)]).limit(top);

#find top N quotes by Price Volatility from yearLow or yearHigh     
def findTopN(top=20,condition=settings.HIGHER):
    if condition == settings.HIGHER:
        result =  findByYearLow(top)
    else:
        result =  findByYearHigh(top)
    stocks = []
    for stock in result:
        code = stock.get('code')
        s = Stock(code)
        if condition == settings.HIGHER:
            s.PercentChangeFromYearLow = stock.get('percentFromYearLow')
        else:
            s.PercentChangeFromYearHigh = stock.get('percentFromYearHigh')
        s.yearHigh = stock.get('yearHigh')
        s.yearLow = stock.get('yearLow')
        s.current = stock.get('current')
        s.ma50 = stock.get('ma50')
        s.ma200 = stock.get('ma200')
        s.name = stock.get('name')

        if code.startswith('6'):
            s.isInSh = True;
        
        #triggered = checkStockWithMA(code,40,10,condition) 
        #print triggered
        
        stocks.append(s)
    return stocks
    #    for stock in result:
#        #print stock.yearHighLow()
#        print stock


#find quote by code     
def findQuoteByCode(code,condition=settings.HIGHER):
    connection = Connection()
    db = connection.stock
    historyDatas = db.tickers
    stock = historyDatas.find_one({"code":code});
    code = stock.get('code')
    s = Stock(code)

    if condition == settings.HIGHER:
        s.PercentChangeFromYearLow = stock.get('percentFromYearLow')
    else:
        s.PercentChangeFromYearHigh = stock.get('percentFromYearHigh')
    s.yearHigh = stock.get('yearHigh')
    s.yearLow = stock.get('yearLow')
    s.current = stock.get('current')
    s.ma50 = stock.get('ma50')
    s.ma200 = stock.get('ma200')
    if code.startswith('6'):
        s.isInSh = True;            
    
    return s

    
if __name__ == '__main__':
    from stocktrace.stock import Stock
    stock = Stock('600880')
    print findQuoteByCode('600327').yearHighLow()
    print findQuoteByCode('600327',settings.LOWER).yearHighLow()
    #findAllNonExistentTickers()
    #updateTickerWithKeyStats('600004',14.00,2.36,0.56,2333.5)
#    stocks = findAllExistentTickers()
#    for stock in stocks:
#       updateTickerWithKeyStats(stock,14.00,2.36,0.56,2333.5)
    #print getMarketPe();
#    print getAvgPe();
#    print getAvgPb();
#    print getPbLessThan1()
#    stocks =['600000', '600004', '600005']
#    batchInsertTicker(stocks)
#    print findLastUpdate('600890')
#    print countByCode('600655')
#    stocks = findStockByCode('600655')
#    for stock in stocks:
#        print stock
    #print findLastStockByDays('600327',10)
#    print findPeakStockByDays('600327',10)
#    print findBottomStockByDays('600327',10)
#    result = findStockByGroup()
#    print len(result)
#    print result[1]['list']
    print findTopN()[0].yearHighLow()
    print findTopN(condition=settings.LOWER)[0].yearHighLow()
    #findPeakStockByDays('600327',10)
#    result = findByYearLow(5)
#    for stock in result:
#        #print stock.yearHighLow()
#        print stock
#    result = findByYearHigh()
#    print '------------------------'
#    for stock in result:
#        #print stock.yearHighLow()
#        print stock
#    peak =  findPeakStockByDays('603000',9,'2012-05-06')
#    print peak
#    for stock in stocks:
#        print stock
#    peak =  findPeakStockByDays('000776',200)
#    print peak
    #print triggerNhNl('600087',52*7,7,'2012-05-06')
