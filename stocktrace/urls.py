from django.conf.urls import patterns, include, url
from zytj import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),
    url(r'^zytj/', include('zytj.urls')),
    url(r'^portfolio/', include('portfolio.urls', namespace='portfolio')),
    url(r'^api/', include('api.urls', namespace='api')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
