from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xmms2_django.song_storage.views',
    # Library files
    (r'add/(?P<song_id>\d+)/$', 'add'),
    (r'artists/$', 'artists'),
    (r'albums/$', 'albums'),
    (r'albums/(?P<artist>\w+)/$', 'albums'),
    (r'edit/(?P<song_id>\d+)/$', 'edit'),
    (r'songs/$', 'songs'),
    (r'by_album/(?P<album>\w+)/$', 'songs'),
    (r'songs/(?P<artist>\w+)/$', 'songs'),
    (r'songs/(?P<artist>\w+)/(?P<album>\w+)/$', 'songs'),
    (r'upload/$', 'upload'),
    (r'$', 'library'),
)
