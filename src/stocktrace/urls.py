from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^zytj/$', 'zytj.views.index'),
    #candlestick chart
    url(r'^zytj/jsoncandle', 'zytj.views.jsoncandle'),
    url(r'^zytj/candle/(\d{6})/jsoncandle', 'zytj.views.jsoncandle'),
    #url(r'^zytj/candle', 'zytj.views.candlestick'),
    #support quote as parameter
    url(r'^zytj/candle/(\d{6})/$', 'zytj.views.candlestick'),
    #NHNL Index
    url(r'^zytj/jsonnhnl', 'zytj.views.jsonnhnl'),
    url(r'^zytj/nhnl', 'zytj.views.nhnl'),
    #MA Index
    url(r'^zytj/ma', 'zytj.views.ma'),
    #Order by 52 week high/low percentage
    url(r'^zytj/alist/ma/(\d{2})/$', 'zytj.views.alist_days_ma'),#asc by days on MA
    url(r'^zytj/alist/(\d{2})/$', 'zytj.views.alist_days'),#asc by days on MA
    url(r'^zytj/alist', 'zytj.views.ascendinglist'),  #asc from year low
    url(r'^zytj/dlist', 'zytj.views.descendinglist'), #des from year high
    url(r'^zytj/quotes', 'zytj.views.quotes'),#show all quotes
    url(r'^zytj/delete', 'zytj.views.delete_stock'),#delete stock
    
    # url(r'^$', 'stocktrace.views.home', name='home'),
    # url(r'^stocktrace/', include('stocktrace.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)
