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
    
def json(request):
#    t = loader.get_template('jquery.jqplot/examples/candlestick-charts.html')
#    c = Context({})
    #return HttpResponse(t.render(c)) 
    ohlc = [
      ["05/09/2009", 136.01, 139.5, 134.53, 139.48],
      ['05/08/2009', 143.82, 144.56, 136.04, 136.97],      
    ];
    return HttpResponse(simplejson.dumps(ohlc), mimetype='application/json')

