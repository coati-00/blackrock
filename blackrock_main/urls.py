from django.conf.urls.defaults import patterns


urlpatterns = patterns('',
                      (r'^loadsolrpoll$',
                       'blackrock.blackrock_main.views.loadsolr_poll'),
                      (r'^previewsolr$',
                       'blackrock.blackrock_main.views.previewsolr'),
                       )
