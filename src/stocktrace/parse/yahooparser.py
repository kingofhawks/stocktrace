'''
Created on 2011-3-7

@author: simon
'''
import sys, traceback
from datetime import date
from datetime import datetime
from datetime import timedelta
from stocktrace.stock import Stock
from lxml import etree
from lxml.html import parse
from stocktrace.dao.stockdao import *
import io
from stocktrace.util import slf4p,settings
import redis

logger = slf4p.getLogger(__name__)
redclient = redis.StrictRedis(host=settings.REDIS_SERVER, port=6379, db=0)

#parse ticker code/name from yahoo finance,check whether exists
def parseTickers(begin=600000,end=603366):
    nonExistentTickers = findAllNonExistentTickers()
    existingTickers = findAllExistentTickers()
    print nonExistentTickers
    print existingTickers
    #parse shanghai tickers
    for code in range(begin,end+1):
        if (str(code) in nonExistentTickers):
            print 'Non-existent ticker***'+str(code)
            continue;
        elif (str(code) in existingTickers):
            print 'Existing ticker***'+str(code)
            continue;
        code2 = str(code) +'.SS'
        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22'+code2+'%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
        print url
        page = parse(url).getroot()
        if page is None:
            print "Fail to query for "+str(code)
            return
        r = page.xpath('//errorindicationreturnedforsymbolchangedinvalid');
       
        errorMsg = r[0].text
        stock = Stock(str(code))
            
        if (errorMsg is None):
            stock.name = ''
            high = page.xpath('//dayshigh')[0].text
            if (high is None):
                print 'Non-existent ticker***'+str(code)
                saveNonExistentTicker(stock)
                continue;
            stock.high = float(high)
            stock.low = float(page.xpath('//dayslow')[0].text)
            stock.yearHigh = float(page.xpath('//yearhigh')[0].text)
            stock.yearLow = float(page.xpath('//yearlow')[0].text)
            close = page.xpath('//bid')[0].text;
#            print close
#            print type(close)
            if close is not None:
                stock.close = float(close)
            if (stock.high>=stock.yearHigh):
                print 'stock trigger new high index*****'+code2 
                with io.open('nh.xml','wb') as f:
                   f.writelines(code2)                    
            elif (stock.low <=stock.yearLow):
                print 'stock trigger new low index*****'+code2
                with io.open('nl.xml','wb') as f:
                   f.writelines(code2)  
            #print stock
            saveTicker(stock)
            
            #parse key statistics data from reuters
            from reutersparser import parseKeyStatData
            parseKeyStatData(code)
        else:
            saveNonExistentTicker(stock)
            print 'Non-existent ticker***'+str(code)
    print 'Finish parseTickers******'

    
    
#parse real time stock price from yahoo finance
def parseFinanceData(code):
    from lxml import etree
    from lxml.html import parse
    if (len(code) == 9):
        code2 = code
    elif (code.startswith('6')):
        code2 = code +".SS"
    else:
        code2 = code +".SZ"
        
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22'+code2+'%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&diagnostics=true'
    logger.debug(url)
        
    try:
        page = parse(url).getroot()
        result = etree.tostring(page)
        print result
        
        r = page.xpath('//errorindicationreturnedforsymbolchangedinvalid');
        errorMsg = r[0].text
        if (errorMsg is None):
            print 'OK'
            stock = Stock(code)
            stock.name = ''
        else:
            print 'error'
        
        quote = page.xpath('/html/body/query/results/quote');
        #print len(quote)    
        #print len(page.xpath('//ask'))
        #print page.xpath('/html/body/query/results/quote/ask[1]/text()')
        #print page.xpath('//ask[1]/text()')[0]#both works
        
        yearLow = page.xpath('//yearlow[1]/text()')[0]
        print 'yearLow'+yearLow
        yearHigh = page.xpath('//yearhigh[1]/text()')[0]
        print 'yearHigh'+yearHigh
        PercentChangeFromYearLow = page.xpath('//percentchangefromyearlow[1]/text()')[0]
        print 'PercentChangeFromYearLow'+PercentChangeFromYearLow
        PercebtChangeFromYearHigh = page.xpath('//percebtchangefromyearhigh[1]/text()')[0]
        print 'PercebtChangeFromYearHigh'+PercebtChangeFromYearHigh
        FiftydayMovingAverage = page.xpath('//fiftydaymovingaverage[1]/text()')[0]
        print 'FiftydayMovingAverage'+FiftydayMovingAverage
        TwoHundreddayMovingAverage = page.xpath('//twohundreddaymovingaverage[1]/text()')[0]
        print 'TwoHundreddayMovingAverage'+TwoHundreddayMovingAverage
        PercentChangeFromTwoHundreddayMovingAverage = page.xpath('//percentchangefromtwohundreddaymovingaverage[1]/text()')[0]
        print 'PercentChangeFromTwoHundreddayMovingAverage'+PercentChangeFromTwoHundreddayMovingAverage
        PercentChangeFromFiftydayMovingAverage = page.xpath('//percentchangefromfiftydaymovingaverage[1]/text()')[0]
        print 'PercentChangeFromFiftydayMovingAverage'+PercentChangeFromFiftydayMovingAverage
        
        stock = Stock(code)
        stock.yearHigh = float(yearHigh)
        stock.yearLow = float(yearLow)
        #stock.PercebtChangeFromYearHigh = float(PercebtChangeFromYearHigh.rstrip('%'))
        stock.PercentChangeFromYearHigh = float(PercebtChangeFromYearHigh.lstrip('-').rstrip('%'))
        stock.PercentChangeFromYearLow = float(PercentChangeFromYearLow.lstrip('+').rstrip('%'))        
        stock.ma50 = float(FiftydayMovingAverage)
        stock.ma200 = float(TwoHundreddayMovingAverage)
        close = page.xpath('//bid')[0].text;
        
        if close is not None:
            stock.close = float(close)
             
        return stock  
    except:
        logger.error('Fail to download latest update from yahoo API:'+code)
        traceback.print_exc(file=sys.stdout) 
        return None 

#get history data from yahoo finance API 
#http://developer.yahoo.com/yql/console/   
def getHistorialData(code,save = True,beginDate = '',endDate = str(date.today())):
    from lxml import etree
    from lxml.html import parse
    #yahoo stock ticker need post-fix ".SS" for Shanghai,'.SZ' for shenzheng
    if (len(code) == 9):
        code2 = code
    elif (code.startswith('6')):
        code2 = code +".SS"
    else:
        code2 = code +".SZ"
#    if len(endDate) == 0:
#        print "Download all history date for "+code
#        from datetime import date
#        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%22'+beginDate+'%22%20and%20endDate%20%3D%20%22'+str(date.today())+'%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
#    else:
#        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%22'+beginDate+'%22%20and%20endDate%20%3D%20%22'+endDate+'%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22'+code2+'%22%20and%20startDate%20%3D%20%22'+beginDate+'%22%20and%20endDate%20%3D%20%22'+endDate+'%22&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'    
    logger.debug(url)
    
    #check whether data is update to latest
    #from stocktrace.dao.stockdao import findLastUpdate
    #from stocktrace.dao.stockdao import findOldestUpdate
    lastStock = findLastUpdate(code)
    oldestStock = findOldestUpdate(code)
#    print lastStock
#    print oldestStock
#    print date.today().weekday()
#    print beginDate    
    #check whether beginDate is weekday 
    begin = datetime.strptime(beginDate,'%Y-%m-%d').date()
    beginWeekday = begin.weekday()
    if (beginWeekday == 5):
        delta = timedelta(2)
        begin = begin+delta
    elif (beginWeekday == 6):
        delta = timedelta(1)
        begin = begin+delta
 #   print begin.weekday()
    beginDate = str(begin)
    isUpdatedToDate = False
    if lastStock is None and oldestStock is None:
        print 'Begin to download history data for '+code
    else:
        print code+" Current history data range "+oldestStock['date']+"~"+lastStock['date']
        isUpdatedToDate = (endDate <= lastStock['date']) and (beginDate >= oldestStock['date'])
    if isUpdatedToDate:
        print "History data is updated to latest:"+code
        return
        
    page = parse(url).getroot()
    result = etree.tostring(page)
    print result
    
    r = page.xpath('//quote');
    historyDatas = []

    for a in r:  
        tree= etree.ElementTree(a)  
        #print etree.tostring(tree) 

        stock = Stock(code)           
        stock.date = tree.xpath('//date')[0].text
        stock.high = float(tree.xpath('//high')[0].text)
        stock.low = float(tree.xpath('//low')[0].text)  
        stock.openPrice = float(tree.xpath('//open')[0].text)
        stock.close = float(tree.xpath('//close')[0].text)
        stock.volume = float(tree.xpath('//volume')[0].text)
        
        isNewData = True;
        if lastStock is not None:            
            isNewData = (stock.date > lastStock['date']) or (stock.date < oldestStock['date'])
        #print stock.date+'***isNewData***'+str(isNewData)
        if isNewData and save:  
            saveStock(stock);
        #print stock    
        historyDatas.append(stock) 
    historyDatas.sort(key=lambda item:item.date,reverse=True) 
    
    if (len(historyDatas) == 0):
        print "No data downloaded for "+code
    else:
        logger.info(str(len(historyDatas))+" history Data downloaded for "+code)
        # redclient.set(code,historyDatas[0].date)
        
#    for stock in historyDatas:
#        print stock 
#    pass 
    
    for i in  range(len(historyDatas)):
        if i == len(historyDatas)-1:
            continue
        else:
            last = historyDatas[i]
            prev = historyDatas[i+1]
            if (last.openPrice!= prev.close and
                (last.low >prev.high or last.high<prev.low)):
                #print "gap***"+last.__str__()   
                pass            
                         

#parse all history data from yahoo
def parseAllHistoryData(file):
    import io
    with io.open(file,'rb') as f:
        list = [];
        for i in range(1000):
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
                    print l; 
                    continue
                
               #parse code
                try:
                    getHistorialData(code,True,'2011-01-01')                                       
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue       
                

        pass

#Download all history data from yahoo via invalid code in DB
def downloadHistoryData(stocks = findAllExistentTickers(),beginDate='2012-01-01',engine=settings.CSV_ENGINE):
    logger.info('current quote size:'+str(len(stocks)))
#    for stock in stocks:
#        #parse code
#        try:
#            getHistorialData(str(stock),True,beginDate)                                       
#        except:
#            traceback.print_exc(file=sys.stdout)
#            continue
    
    import multiprocessing as mp
    pool = mp.Pool(5)
    for stock in stocks:
        pool.apply_async(download_history_data, args = [str(stock),True,beginDate,engine])
    pool.close()
    pool.join()
    
    
def download_history_data(code, save=True, begin_date='2012-01-01', engine=settings.CSV_ENGINE):
    try:
        #latest= redclient.get(code)
        latest = begin_date
        last_update = findLastUpdate(code)
        if last_update is not None:
            latest = last_update['date']
        logger.debug(latest)
        # latest = None
        today = date.today()
        yesterday = date.today()+timedelta(-1)
        if latest is None:
            latest = begin_date
        elif latest == str(today) or latest == str(yesterday):
            logger.info(code+" is already update to latest")
            return

        if engine == settings.CSV_ENGINE:
            getCSVHistorialData(code,save,latest)
        else:
            getHistorialData(code, save, latest)
                                            
    except Exception, e:
        traceback.print_exc(file=sys.stdout)
        logger.exception(e)
        logger.warn('Fail to download history data for:'+code)
        traceback.print_exc(file=sys.stdout) 
        
        
        
#get history data from yahoo CSV API 
# http://ichart.finance.yahoo.com/table.csv?s=300072.sz&d=7&e=23&f=2010&a=5&b=11&c=2010   
def getCSVHistorialData(code,save = True,beginDate = '',endDate = str(date.today())):
    from lxml import etree
    #yahoo stock ticker need post-fix ".SS" for Shanghai,'.SZ' for shenzheng
    if (len(code) == 9):
        code2 = code
    elif (code.startswith('6')):
        code2 = code +".SS"
    else:
        code2 = code +".SZ"

    begin = beginDate.split('-')
    end = endDate.split('-')
    period = '&d='+(str)(int(end[1])-1)+'&e='+end[2]+'&f='+end[0]+'&a='+(str)(int(begin[1])-1)+'&b='+begin[2]+'&c='+begin[0]    
    url = 'http://ichart.finance.yahoo.com/table.csv?s='+code2+period
    logger.debug(url)
    
    #check whether data is update to latest
    #from stocktrace.dao.stockdao import findLastUpdate
    #from stocktrace.dao.stockdao import findOldestUpdate
    lastStock = findLastUpdate(code)
    oldestStock = findOldestUpdate(code)
            
    page = parse(url).getroot()
    logger.debug(page)
    result = etree.tostring(page)
    #print result
    lines = result.split('\n')
    
    from stocktrace.stock import Stock
    historyDatas = []

    for a in lines:  
        if a.find('html')!= -1:
            continue        
        #print etree.tostring(tree) 

        datas = a.split(',')
        #print datas
        stock = Stock(code)           
        stock.date = datas[0]
        stock.high = float(datas[2])
        stock.low = float(datas[3])  
        stock.openPrice = float(datas[1])
        stock.close = float(datas[4])
        stock.volume = float(datas[5])
        
        isNewData = True;
        if lastStock is not None:            
            isNewData = (stock.date > lastStock['date']) or (stock.date < oldestStock['date'])
        #print stock.date+'***isNewData***'+str(isNewData)
        if isNewData and save:  
            saveStock(stock);
        #print stock    
        historyDatas.append(stock) 
    historyDatas.sort(key=lambda item:item.date,reverse=True) 
    
    if (len(historyDatas) == 0):
        logger.warning("No data downloaded for "+code)
    else:
        update_week52(code)
        logger.info(str(len(historyDatas))+" history Data downloaded for "+code)
        
       
   
    
#lastDays: the last range to check the index,default will be 1 year's data(52 weeks),i.e,the sampling period
#newDays: the latest days trigger the index
#ex. computeNhnlIndex(file,360,3,2012-05-02) will check the 360 days trading record before 2012-05-02,
#to check if the price during the nearest 3 days trigger NH-NL index
def computeNhnlIndex(file,lastDays,nearDays,endDate = str(date.today())):
    result = {}
    import io
    with io.open(file,'rb') as f:
        nhList = [];
        nlList = [];
        nhCount = 0;
        nlCount = 0;
        for i in range(1000):
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
                    print l; 
                    continue
                
               #parse code
                try:
                    #from stocktrace.dao.stockdao import triggerNhNl
                    triggered = triggerNhNl(code,lastDays,nearDays,endDate)   
                    if triggered == 1:
                        nhCount += 1;
                        nhList.append(code)
                    elif triggered == -1:
                        nlCount += 1;     
                        nlList.append(code)                                                   
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue       
        
        print "currentDate****"+endDate
        print 'nhCount ****'+str(nhCount)+str(nhList)
        print 'nlCount ****'+str(nlCount)+str(nlList)
        result[endDate] = {'nhnl':nhCount-nlCount,'nhList':nhList,'nlList':nlList}

        return result

#lastDays: the last range(history data) to check the index,default will be 1 year's data(52 weeks),i.e,the sampling period
#newDays: the latest days trigger the index
#ex. computeNhnlIndex(file,360,3,2012-05-02) will check the 360 days trading record before 2012-05-02,
#to check if the price during the nearest 3 days trigger NH-NL index
def computeNhnlIndexWithStocks(stocks,lastDays,nearDays,endDate = str(date.today())):
    #result = []
    result = {}
    nhList = [];
    nlList = [];
    nhCount = 0;
    nlCount = 0;
    for code in stocks:
        #parse code
                try:
                    triggered = triggerNhNl(code,lastDays,nearDays,endDate) 
                    #print triggered
                    if triggered == 0:
                        continue
                    elif triggered.get('value') == 1:
                        nhCount += 1;
                        nhList.append(code)
                    elif triggered.get('value') == -1:
                        nlCount += 1;     
                        nlList.append(code)
                                                                                            
                except:
                    traceback.print_exc(file=sys.stdout)
                    continue           
        
    print "currentDate****"+endDate
    print 'nhCount ****'+str(nhCount)+str(nhList)
    print 'nlCount ****'+str(nlCount)+str(nlList)
    #result.append({'date':endDate,'nhnl':nhCount-nlCount,'nhList':nhList,'nlList':nlList})
    result['date'] = endDate
    result['nhnl'] = nhCount-nlCount
    result['nhList'] = nhList
    result['nlList'] = nlList
    return result

#compute the NHNL index between beginDate and endDate
def computeNhnlIndexWithinRange(file,lastDays,nearDays,beginDate = str(date.today()),endDate = str(date.today())):
    period =  (datetime.strptime(endDate,'%Y-%m-%d')-datetime.strptime(beginDate,'%Y-%m-%d')).days
    for i in range(period):
        currentDay = datetime.strptime(beginDate,'%Y-%m-%d').date()+timedelta(i)
        print computeNhnlIndex(file,lastDays,nearDays,str(currentDay))       
    pass    

#compute the NHNL index between beginDate and endDate
def computeNhnlIndexWithinRangeWithStocks(stocks,lastDays,nearDays,beginDate = str(date.today()),endDate = str(date.today())):
    period =  (datetime.strptime(endDate,'%Y-%m-%d')-datetime.strptime(beginDate,'%Y-%m-%d')).days+1
    result = []
    print period
    for i in range(period):
        currentDay = datetime.strptime(beginDate,'%Y-%m-%d').date()+timedelta(i)
        print 'now***'+str(currentDay)+str(i)
        temp = computeNhnlIndexWithStocks(stocks,lastDays,nearDays,str(currentDay))
        #print temp
        result.append(temp)        
    return result                  
                    
if __name__ == '__main__':
    stocks = ['600327','600829','600573','600369','601688','600132','600332','601866','600718','600048']
    #parseTickers();
    print parseFinanceData('600327')
    #print getCSVHistorialData('600327',beginDate='2012-01-01')
    #getHistorialData('000001.SS',beginDate='2012-04-01')
    #getHistorialData('600327',beginDate='2012-04-01')
    #triggered = triggerNhNl('600655',200,5) 
#    for stock in stocks:
#        getHistorialData(stock,beginDate='2012-04-01')
    #print computeNhnlIndexWithinRangeWithStocks(stocks,60,7,'2012-04-01')
    #getHistorialData('600327',True,'2011-01-01')
    #parseAllHistoryDataInDB()
#    parseAllHistoryData('stock_list_all')
    #computeNhnlIndex('stock_list_all',52*7,7)
#    computeNhnlIndexWithinRange('stock_list',52*7,7,'2012-01-01')
    
#    from dao.stockdao import findAllStocks
#    findAllStocks();
#                
#    import logging
#    LOG_FILENAME = 'example.log'
#    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
#
#    logging.error('This message should go to the log file')
