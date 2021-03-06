from django.conf.urls import patterns, url

urlpatterns = patterns(
    'blackrock.waterquality.views',
    url(r'^$', 'index', name='waterchemistry-index'),
    url(r'^graph/$', 'graphing_tool', name='waterchemistry-graphing-tool'),
    url(r'^browse/$', 'browse', name='waterchemistry-browse'),
    url(r'^series/(?P<id>\d+)/$', 'series', name='waterchemistry-series'),
    url(r'^series/(?P<id>\d+)/all/$',
        'series_all', name='waterchemistry-series-all'),
    url(r'^series/(?P<id>\d+)/verify/$',
        'series_verify', name='waterchemistry-series-verify'),
    url(r'^teaching/$', 'teaching', name='waterchemistry-teaching'),
)
