from django.conf.urls.defaults import *

urlpatterns = patterns('waterquality.views',
                       url(r'^$','index',name='waterquality-index'),
                       url(r'^browse/$','browse',name='waterquality-browse'),
                       url(r'^series/(?P<id>\d+)/$','series',name='waterquality-series'),
                       url(r'^series/(?P<id>\d+)/all/$','series_all',name='waterquality-series-all'),
)