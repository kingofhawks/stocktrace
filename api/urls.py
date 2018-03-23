from django.conf.urls import url
from api.views import *
from django.urls import path

app_name = 'url'
urlpatterns = [
    # Examples:
    url(r'^csi', IndexView.as_view()),
    url(r'^industry', IndustryView.as_view()),
    url(r'^equity', EquityView.as_view()),
    url(r'^ah', AhView.as_view()),
    url(r'^sw', SwView.as_view()),
    url(r'^stock', StockView.as_view()),
    url(r'^diff', diff),
    url(r'^sh', sh),
    url(r'^cix', CixView.as_view())
]
