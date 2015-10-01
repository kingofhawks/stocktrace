from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.stock_list, name='home'),
    url(r'^history', views.history, name='history'),
    url(r'^create', views.create_stock),
    url(r'^detail', views.detail),
    url(r'^portfolio_detail/(?P<pk>\w+)/$', views.portfolio_detail, name='portfolio_detail'),
    url(r'^update', views.update),
    url(r'^stock/(?P<pk>\d{6})/delete/$', views.delete, name='delete'),
    url(r'^(?P<pk>\w+)/delete/$', views.delete_portfolio, name='delete_portfolio'),
    url(r'^tag/(?P<pk>\w+)/$', views.tag),
    url(r'^snapshot', views.snapshot_view, name='snapshot'),

)
