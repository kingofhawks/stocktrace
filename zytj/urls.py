from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index),
    #candlestick chart
    url(r'^jsoncandle', views.jsoncandle),
    url(r'^candle/(\d{6})/jsoncandle', views.jsoncandle),
    #url(r'^zytj/candle', 'zytj.views.candlestick'),
    #support quote as parameter
    url(r'^candle/(\d{6})/$', views.candlestick),
    #NHNL Index
    url(r'^jsonnhnl', views.jsonnhnl),
    url(r'^nhnl', views.nhnl, name='zytj.nhnl'),
    #MA Index
    url(r'^ma', views.ma, name='zytj.ma'),
    #Order by 52 week high/low percentage
    url(r'^alist/ma/(\d{2})/$', views.alist_days_ma),#asc by days on MA
    url(r'^alist/(\d{2})/$', views.alist_days),#asc by days on MA
    url(r'^alist', views.ascendinglist, name='zytj.alist'),  #asc from year low
    url(r'^dlist', views.descendinglist, name='zytj.dlist'), #des from year high
    url(r'^quotes', views.quotes),#show all quotes
    url(r'^delete', views.delete_stock),#delete stock

    
)
