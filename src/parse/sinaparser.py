#!/usr/bin/env python

import thread
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
    print stock
    return stock
    
    #print '%.2f'%percent+'%'   
    #print sys.argv[0]    
    
def getMyStock():
    codes = ['sh600327','sh600739','sh600583','sh600573','sh601866','sh000001']
    
    for code in codes: 
        getStock(code)
        #thread.start_new(getStock,(code,))
if __name__ =="__main__":    
    import time, os, sys, sched
    schedule = sched.scheduler(time.time, time.sleep)
    schedule.enter(0, 0, getMyStock, ())   # 0==right now
    schedule.run( )
    #getMyStock()    
    import urllib2
    h=urllib2.HTTPHandler(debuglevel=1)    
    request = urllib2.Request('http://finance.google.com/finance/info?q=600030')
    request.add_header('User-Agent','StockTrace/1.0') 
    opener = urllib2.build_opener(h) 
    #feeddata = opener.open(request).read()  
    #print feeddata
    #print os.path.abspath(os.path.dirname(sys.argv[0]))
    #print sys.argv[0]
    
