from django.conf.urls import include, url
from zytj import views as zyt_views
from base import views as base_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', zyt_views.index, name='index'),
    url(r'^$', base_views.index, name='index'),
    url(r'^zytj/', include('zytj.urls')),
    url(r'^portfolio/', include('portfolio.urls', namespace='portfolio')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^market/', include('market.urls', namespace='market')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
]

