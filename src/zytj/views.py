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
    return render(request,'ajax.html',
                  {'ohlc':ohlc})   
    

def jsoncandle(request):
    from dao.stockdao import findLastStockByDays
    stocks = findLastStockByDays('600327',60)
    ohlc = []
    for stock in stocks:
      #print stock
      s = []
      s.append(stock['date'])
      s.append(stock['open'])
      s.append(stock['high'])
      s.append(stock['low'])
      s.append(stock['close'])
      print s
      ohlc.append(s)
    print ohlc  
#    ohlc = [
#      ["2009-04-09", 136.01, 139.5, 134.53, 139.48],
#      ['2009-04-08', 143.82, 144.56, 136.04, 136.97],      
#    ];
    return HttpResponse(simplejson.dumps(ohlc), mimetype='application/json')

def candlestick(request):
    return render(request,'candlestick.html')   

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

