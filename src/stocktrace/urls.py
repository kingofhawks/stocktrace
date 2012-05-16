from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^zytj/$', 'zytj.views.index'),
    url(r'^zytj/json', 'zytj.views.json'),
    # url(r'^$', 'stocktrace.views.home', name='home'),
    # url(r'^stocktrace/', include('stocktrace.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
