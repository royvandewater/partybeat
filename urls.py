from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^xmms2_django/', include('xmms2_django.foo.urls')),

    (r'^$', 'xmms2_django.main.views.player'),
    # (r'^action/(?P<action>\w+)/$', 'xmms2_django.player.views.run_action'),
    # (r'^refresh/$', 'xmms2_django.player.views.refresh'),
    # (r'^info/$', 'xmms2_django.player.views.get_info'),
    # (r'^playlist/$', 'xmms2_django.player.views.playlist'),
    # (r'^fix/$', 'xmms2_django.player.views.fix'),
    # (r'^delete/(?P<xmms_id>\d+)/$', 'xmms2_django.player.views.delete'),

    # Library files
    (r'^library/$', 'xmms2_django.song_storage.views.library'),
    (r'^library/artists/$', 'xmms2_django.song_storage.views.artists'),
    (r'^library/albums/$', 'xmms2_django.song_storage.views.albums'),
    (r'^library/albums/(?P<artist>\w+)/$', 'xmms2_django.song_storage.views.albums'),
    (r'^library/songs/$', 'xmms2_django.song_storage.views.songs'),
    (r'^library/by_album/(?P<album>\w+)/$', 'xmms2_django.song_storage.views.songs'),
    (r'^library/songs/(?P<artist>\w+)/$', 'xmms2_django.song_storage.views.songs'),
    (r'^library/songs/(?P<artist>\w+)/(?P<album>\w+)/$', 'xmms2_django.song_storage.views.songs'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
