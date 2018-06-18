from django.conf.urls import url
import market.views as views

app_name = 'market'
urlpatterns = [
    url(r'^sw', views.sw, name='sw'),
    url(r'^csi', views.cs_index, name='csi'),
    url(r'^industry', views.industry, name='industry'),
    url(r'^equity', views.equity, name='equity'),
    url(r'^history', views.history, name='history'),
    url(r'^diff', views.diff, name='diff'),
    url(r'^sh', views.sh, name='sh'),
]
