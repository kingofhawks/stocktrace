from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^sw', views.sw, name='sw'),

)
