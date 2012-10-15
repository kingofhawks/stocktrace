# Create your views here.
from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse
from django.http import Http404

def index(request):
#    t = loader.get_template('jquery.jqplot/examples/candlestick-charts.html')
#    c = Context({})
    #return HttpResponse(t.render(c)) 
    ohlc = [
      ["06/09/2009", 136.01, 139.5, 134.53, 139.48],
      ['06/08/2009', 143.82, 144.56, 136.04, 136.97],      
    ];
    return render(request,'index.html',
                  {'ohlc':ohlc})   
    
#q:quote code
def jsoncandle(request,q):
    try:
        print q
    #    quote = request.GET.get('q', 'test')
    #    print request.GET
    #    print quote    
        
        from stocktrace.dao.stockdao import findLastStockByDays
        stocks = findLastStockByDays(q,60)
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
                print ohlc[j][4]
                ma5sum = ma5sum +ohlc[j][4]
            ma5.append(ma5sum/5)
            print ma5
            ma4.append(ma5)
    except:
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
    
    return HttpResponse(simplejson.dumps([ohlc,ma1,ma2,ma3,ma4]), mimetype='application/json')

#q:stock code,which will be passed to jsoncandle()
def candlestick(request,q):
    return render(request,'candlestick.html') 

#def candlestick(request):
#    return render(request,'candlestick.html')   


def jsonnhnl(request):
    from stocktrace.parse.yahooparser import computeNhnlIndexWithinRangeWithStocks
    stocks = ['600327','600573','600583','600600','600221','601111','600718']
    result = computeNhnlIndexWithinRangeWithStocks(stocks,60,7,'2012-09-01')
    print result
    data = []
    for record in result:
      print record
      s = []
      s.append(record['date'])
      s.append(record['nhnl'])      
      data.append(s)
    print data  
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def nhnl(request):
    return render(request,'nhnl-index.html') 

def ma(request):
    return render(request,'ma.html') 


