from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^sw', views.sw, name='sw'),
    url(r'^history', views.history, name='history'),
    url(r'^diff', views.diff, name='diff'),
)
