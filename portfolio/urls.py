from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.stock_list2, name='home'),
    url(r'^create', views.create_stock),
    url(r'^detail', views.detail),
    url(r'^update', views.update),
    url(r'^stock/(?P<pk>\d{6})/delete/$', views.delete, name='delete'),
    url(r'^tag/(?P<pk>\w+)/$', views.tag),

)
