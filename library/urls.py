from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('partybeat.library.views',
    # Library files
    (r'add/random/$', 'add_random'),
    (r'add/(?P<song_id>\d+)/$', 'add'),
    (r'edit/(?P<song_id>\d+)/$', 'edit'),
    (r'download/(?P<song_id>\d+)/$', 'download'),
    (r'upload/$', 'upload'),
    (r'search/$', 'search'),
    (r'albums/$', 'albums'),
    (r'albums/artist/(?P<artist>\w+)/$', 'albums'),
    (r'artists/$', 'artists'),
    (r'songs/$', 'songs'),
    (r'songs/album/(?P<album>\w+)/$', 'songs'),
    (r'songs/artist/(?P<artist>\w+)/$', 'songs'),
    (r'songs/artist/(?P<artist>\w+)/album/(?P<album>\w+)/$', 'songs'),
    (r'$', 'library'),
)
