from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^xmms2_django/', include('xmms2_django.foo.urls')),

    (r'^$', 'xmms2_django.main.views.player'),
    (r'^player/', include('xmms2_django.player.urls')),

    # Library files
    (r'^library/', include('xmms2_django.song_storage.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)
