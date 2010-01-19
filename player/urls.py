from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xmms2_django.player.views',

    # Player url patterns
    (r'action/seek/(?P<seek_time>\w+)/$', 'seek'),
    (r'action/(?P<action>\w+)/$', 'run_action'),
    (r'delete/(?P<position>\d+)/$', 'delete'),
    (r'info/$', 'get_info'),
    (r'playlist/$', 'playlist'),
    (r'player/$', 'player'),
)
