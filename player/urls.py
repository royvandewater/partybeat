from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('partybeat.player.views',

    # Player url patterns
    (r'action/seek/(?P<seek_time>\w+)/$', 'seek'),
    (r'action/(?P<action>\w+)/$', 'run_action'),
    (r'action/(?P<action>\w+)/$', 'run_action'),
    (r'delete/(?P<position>\d+)/$', 'delete'),
    (r'volume/(?P<volume>\d+)/$', 'volume'),
    (r'info/$', 'get_info'),
    (r'player/$', 'player'),
    (r'playlist/$', 'playlist'),
    (r'skip_to/(?P<position>\d+)/$', 'skip_to'),
    (r'move/(?P<start>\d+)/to/(?P<end>\d+)/$', 'move'),
    (r'$', 'main'),
)
