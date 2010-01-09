from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^xmms2_django/', include('xmms2_django.foo.urls')),

    (r'^$', 'xmms2_django.main.views.player'),
    (r'^player/action/(?P<action>\w+)/$', 'xmms2_django.player.views.run_action'),
    (r'^player/info/$', 'xmms2_django.player.views.get_info'),
    (r'^player/playlist/$', 'xmms2_django.player.views.playlist'),
    (r'^player/delete/(?P<position>\d+)/$', 'xmms2_django.player.views.delete'),

    # Library files
    (r'^library/', include('xmms2_django.song_storage.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
