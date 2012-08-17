#!/usr/bin/env python

import thread

#quote state cache
stateCache = {}

def getStock(code):
    #Sina API
    url = "http://hq.sinajs.cn/list="+code
    #Google Finance API
    #url = 'http://finance.google.com/finance/info?q=600030'    
    import urllib2,os,sys
    from stock import Stock

    pg = urllib2.urlopen(url)
    cont = pg.read()
    #print cont
    test = cont.split(',')
    yesterday = float(test[2])
    current = float(test[3])
    high = float(test[4])
    low = float(test[5])
    percent = (current-yesterday)/yesterday*100
    stock = Stock(code,current,percent,low,high)
    
    #check threshold
    if (percent >=2):
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
    else:
        stock.alert = False;
        
    return stock
    
    #print '%.2f'%percent+'%'   
    #print sys.argv[0]    
    
def getMyStock(codes = ['sh600327','sh600600','sh601111','sh600221','sh600583','sh600573','sh600428','sh000001']):
    
    stocksCrossThreshold = [] 
    for code in codes: 
        stock = getStock(code)
        print stock
        if (stock.alert == True):
            stocksCrossThreshold.append(stock.shortStr())
        #thread.start_new(getStock,(code,))
    
    if (len(stocksCrossThreshold) !=0):
        from util.mailutil import sendMail
        print stocksCrossThreshold
        sendMail(str(stocksCrossThreshold))
    
    print '******************finished quote polling***********************'

#download latest price info from sina
def downloadLatestData(quotes = ['sh600327','sh600739','sh600583','sh600573','sh601866','sh000001']):
    
    for code in quotes: 
        quote = getStock(code)
        print quote
        
if __name__ =="__main__":    
    import time, os, sys, sched
#    schedule = sched.scheduler(time.time, time.sleep)
#    schedule.enter(0, 0, getMyStock, ())   # 0==right now
#    schedule.run( )
    getMyStock()    
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
    
