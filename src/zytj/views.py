# Create your views here.
from django.shortcuts import render
from django.utils import simplejson
from django.http import HttpResponse

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
    print q
#    quote = request.GET.get('q', 'test')
#    print request.GET
#    print quote    
    
    from dao.stockdao import findLastStockByDays
    stocks = findLastStockByDays(q,60)
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
    #print ohlc  
    #sample format for ohlc
#    ohlc = [
#      ["2012-08-14", 136.01, 139.5, 134.53, 139.48],
#      ['2012-08-13', 143.82, 144.56, 136.04, 136.97],      
#    ];
    return HttpResponse(simplejson.dumps(ohlc), mimetype='application/json')

#q:stock code,which will be passed to jsoncandle()
def candlestick(request,q):
    return render(request,'candlestick.html') 

#def candlestick(request):
#    return render(request,'candlestick.html')   


def jsonnhnl(request):
    from parse.yahooparser import computeNhnlIndexWithinRangeWithStocks
    stocks = ['600327','600829','600573','600369','601688','600132','600332','601866','600718']
    result = computeNhnlIndexWithinRangeWithStocks(stocks,60,7,'2012-04-01')
    print result
    data = []
    for record in result:
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

