from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xmms2_django.song_storage.views',
    # Library files
    (r'$', 'library'),
    (r'add/(?P<song_id>\w+)/$', 'add'),
    (r'artists/$', 'artists'),
    (r'albums/$', 'albums'),
    (r'albums/(?P<artist>\w+)/$', 'albums'),
    (r'songs/$', 'songs'),
    (r'by_album/(?P<album>\w+)/$', 'songs'),
    (r'songs/(?P<artist>\w+)/$', 'songs'),
    (r'songs/(?P<artist>\w+)/(?P<album>\w+)/$', 'songs'),
)
