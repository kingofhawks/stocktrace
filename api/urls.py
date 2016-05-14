from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # Examples:
    url(r'^market', views.MarketView.as_view()),
    url(r'^ah', views.AhView.as_view()),
    url(r'^sw', views.SwView.as_view()),
    url(r'^stock/$', views.StockView.as_view()),
    url(r'^diff', views.diff),
    url(r'^sh', views.sh),
)
