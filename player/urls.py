from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('xmms2_django.player.views',

    # Player url patterns
    (r'action/(?P<action>\w+)/$', 'run_action'),
    (r'info/$', 'get_info'),
    (r'playlist/$', 'playlist'),
    (r'delete/(?P<position>\d+)/$', 'delete'),

)
