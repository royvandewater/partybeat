from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^xmms2_django/', include('xmms2_django.foo.urls')),

    (r'^$', 'xmms2_django.xmms2.views.player'),
    (r'^action/(?P<action>\w+)/$', 'xmms2_django.xmms2.views.run_action'),
    (r'^refresh/$', 'xmms2_django.xmms2.views.refresh'),
    (r'^info/$', 'xmms2_django.xmms2.views.get_info'),
    (r'^playlist/$', 'xmms2_django.xmms2.views.playlist'),
    (r'^fix/$', 'xmms2_django.xmms2.views.fix'),
    (r'^delete/(?P<xmms_id>\d+)/$', 'xmms2_django.xmms2.views.delete'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
