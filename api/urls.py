from django.conf.urls import url
from api.views import *
from django.urls import path

app_name = 'url'
urlpatterns = [
    # Examples:
    url(r'^csi', IndexView.as_view()),
    url(r'^industries', industry_list),
    url(r'^industry', IndustryView.as_view()),
    url(r'^equity', EquityView.as_view()),
    url(r'^equities', equity_list),
    url(r'^indexes', index_list),
    url(r'^ah', AhView.as_view()),
    url(r'^swlist', sw_list),
    url(r'^sw', SwView.as_view()),
    url(r'^stock', StockView.as_view()),
    url(r'^diff', diff),
    url(r'^sh', sh),
    url(r'^market', MarketView.as_view()),
    # url(r'^portfolio', portfolio),
    url(r'^portfolio_history', PortfolioView.as_view()),
    url(r'^rule', portfolio),
    url(r'^fake_chart_data', fake),
]
