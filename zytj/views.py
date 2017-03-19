#-*- coding: UTF-8 -*-

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from stocktrace.util import settings
from stocktrace.dao.stockdao import findTopN,remove_stock
# import redis
from django.core.cache import cache
from stocktrace.util import slf4p
import json
from django.http import HttpResponseRedirect

logger = slf4p.getLogger(__name__)
# redclient = redis.StrictRedis(host=settings.REDIS_SERVER, port=6379, db=0)


def index(request):
#    t = loader.get_template('jquery.jqplot/examples/candlestick-charts.html')
#    c = Context({})
    #return HttpResponse(t.render(c)) 
    ohlc = [
      ["06/09/2009", 136.01, 139.5, 134.53, 139.48],
      ['06/08/2009', 143.82, 144.56, 136.04, 136.97],      
    ];
    
    # return render(request,'index.html',
    #               {'ohlc':ohlc})
    return HttpResponseRedirect('zytj/alist')

#q:quote code
def jsoncandle(request,q):
    try:
        # print q
    #    quote = request.GET.get('q', 'test')
    #    print request.GET
    #    print quote    
        
        from stocktrace.dao.stockdao import findLastStockByDays
        stocks = findLastStockByDays(q,100)
        ohlc = []
        #MA10
        ma1 = []
        #MA20
        ma2 = []
        #MA50
        ma3 = []
        #MA5
        ma4 = []
        
        index = 0;
    
        
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
        #MA10
        for i in range(10,size):
            ma10 = []
            ma10.append(ohlc[i][0])
            
            ma10sum = 0.0;
            for j in range(i-9,i+1):
                ma10sum = ma10sum +ohlc[j][4]
            ma10.append(ma10sum/10)
            #print ma10
            ma1.append(ma10)
            
        #MA20
        for i in range(20,size):
            ma20 = []
            ma20.append(ohlc[i][0])
            
            ma20sum = 0.0;
            for j in range(i-19,i+1):
                ma20sum = ma20sum +ohlc[j][4]
            ma20.append(ma20sum/20)
            #print ma20
            ma2.append(ma20)
            
        #MA50
        for i in range(50,size):
            ma50 = []
            ma50.append(ohlc[i][0])
            
            ma50sum = 0.0;
            for j in range(i-49,i+1):
                ma50sum = ma50sum +ohlc[j][4]
            ma50.append(ma50sum/50)
            #print ma50
            ma3.append(ma50)
        
        #MA5
        for i in range(5,size):
            ma5 = []
            ma5.append(ohlc[i][0])
            
            ma5sum = 0.0;
            for j in range(i-4,i+1):
                # print ohlc[j][4]
                ma5sum = ma5sum +ohlc[j][4]
            ma5.append(ma5sum/5)
            # print ma5
            ma4.append(ma5)
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
        raise Http404
                
    #sample format for ohlc
#    ohlc = [
#      ["2012-08-14", 136.01, 139.5, 134.53, 139.48],
#      ['2012-08-13', 143.82, 144.56, 136.04, 136.97],      
#    ];
#    line = [['06/08/2009', 7], ['06/09/2009', 100],['06/10/2009', 50]];
#    
#    line3 = [
#     ["06/08/2009", 136.01, 139.5, 134.53, 139.48],
#     ["06/09/2009", 143.82, 144.56, 136.04, 136.97],
#     ["06/10/2009", 143.82, 144.56, 136.04, 136.97]
#     ]
#    ohlc =[line3,line]


    #only draw candlestick
    #return HttpResponse(simplejson.dumps(ohlc), mimetype='application/json')
    
    #draw candlestick with multiple MA
    
    return HttpResponse(json.dumps([ohlc,ma1,ma2,ma3,ma4]), content_type='application/json')

#q:stock code,which will be passed to jsoncandle()
def candlestick(request,q):
    return render(request,'candlestick.html') 

#def candlestick(request):
#    return render(request,'candlestick.html')   


def jsonnhnl(request):
    from stocktrace.parse.yahooparser import computeNhnlIndexWithinRangeWithStocks
    stocks = ['600327','600573','600583','600600','600221','601111','600718']
    result = computeNhnlIndexWithinRangeWithStocks(stocks,60,7,'2012-09-01')
    # print result
    data = []
    for record in result:
      # print record
      s = []
      s.append(record['date'])
      s.append(record['nhnl'])      
      data.append(s)
    # print data
    return HttpResponse(json.dumps(data), content_type='application/json')

def nhnl(request):
    return render(request,'nhnl-index.html')

def ma(request):
    return render(request,'ma.html') 

#ascend from year low
def ascendinglist(request):
    return listall(request,settings.HIGHER)

#descend from year high
def descendinglist(request):
    return listall(request,settings.LOWER)

def listall(request,condition):
    dest = 'screen_year_low_high.html'

    cache.set('my_key', 'hello, world!', 30)
    # print cache.get('my_key')
    
    c = request.GET.get('c')
    # print c
    
    if condition == settings.HIGHER:
        orderByAlist = True
    else:
        orderByAlist = False
            
    if c is not None:
        results = []
        from stocktrace.dao.stockdao import findQuoteByCode
        stock = findQuoteByCode(c,condition)
        # print stock.yearHighLow()
        results.append(stock)
        return render(request,dest,{'results':results,'orderByAlist':orderByAlist})
    else:
        q = request.GET.get('q')
        industry = request.GET.get('industry')
        if industry is None:
            industry = 'all'
        # print 'industry:'+industry
        
        if condition == settings.HIGHER:
            topn = findTopN(settings.PAGING_TOTAL);
            context = 'alist'            
        else:
            topn = findTopN(settings.PAGING_TOTAL,settings.LOWER);
            context = 'dlist'         
        
        
            
        from stocktrace.redis.redisservice import filterStocksByIndustry,filterStocksByList  
        #filter stocks by industry  
        topn = filterStocksByIndustry(topn,industry)
        
        stockList = request.GET.get('list')
        if stockList is None:
            stockList = settings.STOCK_LIST_ALL
        logger.debug('stockList:'+stockList)
        #filter stocks by stock list
        import time
        start = time.clock()
        topn = filterStocksByList(topn,stockList)
        finish = time.clock()
        # print finish-start
        import timeit
        # print timeit.timeit('char in text', setup='text = "sample string"; char = "g"')
        
        if q is None:
            results = topn[0:settings.PAGING_ITEM]
        else:
            results = topn[settings.PAGING_ITEM*(int(q)-1):settings.PAGING_ITEM*int(q)]

        logger.debug(results)
        for s in results:
            logger.debug(s.name)
        #print len(results)
        industries = []
        # try:
        #     industries = redclient.zrange(settings.INDUSTRY_SET,0,-1)
        # except:
        #     industries = []
        
        return render(request,dest,{'results':results,'industry':industry,'industry_set':industries,
                                    'lists':settings.ALL_LIST,'stockList':stockList,
                                    'context':context,'orderByAlist':orderByAlist})

#ascending list during last days by MA
def alist_days_ma(request,days):
    from stocktrace.parse.screener import findByMa
    result = findByMa(int(days),10,condition=settings.LOWER)
    # print result
    # print '**************************'
    return render(request,'alist_days_ma.html',{'results':result})

#ascending list during last days by price
def alist_days(request,days):
    from stocktrace.parse.screener import findByMa
    result = findByMa(int(days),10,condition=settings.LOWER)
    # print result
    # print '**************************'
    return render(request,'alist_days.html',{'results':result})

def quotes(request):
    from stocktrace.dao.stockdao import findAllQuotes
    quotes = findAllQuotes()
    jsonData = json.dumps(quotes)
    
    return HttpResponse(jsonData, content_type='application/json')


def delete_stock(request):
    code = request.GET.get('code')
    logger.info('Remove stock:{}'.format(code))
    remove_stock(code)
    return HttpResponse(json.dumps('OK'), content_type='application/json')



