from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xmms2_django.song_storage.views',
    # Library files
    (r'^library/$', 'library'),
    (r'^library/add/(?P<song_id>\w+)/$', 'add'),
    (r'^library/artists/$', 'artists'),
    (r'^library/albums/$', 'albums'),
    (r'^library/albums/(?P<artist>\w+)/$', 'albums'),
    (r'^library/songs/$', 'songs'),
    (r'^library/by_album/(?P<album>\w+)/$', 'songs'),
    (r'^library/songs/(?P<artist>\w+)/$', 'songs'),
    (r'^library/songs/(?P<artist>\w+)/(?P<album>\w+)/$', 'songs'),
)
