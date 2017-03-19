from django.conf.urls import url
import market.views as views


urlpatterns = [
    url(r'^sw', views.sw, name='sw'),
    url(r'^history', views.history, name='history'),
    url(r'^diff', views.diff, name='diff'),
    url(r'^sh', views.sh, name='sh'),
    url(r'^cix', views.cix, name='cix'),
]
