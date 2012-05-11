# Create your views here.
from django.shortcuts import render
def index(request):
#    t = loader.get_template('jquery.jqplot/examples/candlestick-charts.html')
#    c = Context({})
    #return HttpResponse(t.render(c)) 
    ohlc = [
      ['06/15/2009 16:00:00', 136.01, 139.5, 134.53, 139.48],
      ['06/08/2009 16:00:00', 143.82, 144.56, 136.04, 136.97],      
    ];
    return render(request,'index.html',
                  {'ohlc':ohlc})   

