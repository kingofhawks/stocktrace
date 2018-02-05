from django.conf.urls import url
from api.views import *


urlpatterns = [
    # Examples:
    url(r'^index', IndexView.as_view()),
    url(r'^ah', AhView.as_view()),
    url(r'^sw', SwView.as_view()),
    url(r'^stock/$', StockView.as_view()),
    url(r'^diff', diff),
    url(r'^sh', sh),
    url(r'^cix', CixView.as_view())
]
