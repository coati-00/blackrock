from django.conf.urls.defaults import *
import os.path

media_root = os.path.join(os.path.dirname(__file__),"media")

urlpatterns = patterns('',
	(r'^$', 'blackrock.sampler.views.index'),
        (r'^plot$', 'blackrock.sampler.views.plot'),
        (r'^transect$', 'blackrock.sampler.views.transect'),
        (r'^worksheet$', 'blackrock.sampler.views.worksheet'),
        (r'^csv$', 'blackrock.sampler.views.export_csv'),
        (r'^import_csv$', 'blackrock.sampler.views.import_csv'),
        (r'^csv_info$', 'blackrock.sampler.views.csv_info'),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': media_root}),
)

