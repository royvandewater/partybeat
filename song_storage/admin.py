from django.contrib import admin
from xmms2_django.song_storage.models import *

class SongFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'album', 'artist',) # The future listview
    fieldsets = (
            (None, {
                'fields': ('file',)
            }),
            ('Leave blank to extract from id3', {
                'fields': ('name', 'artist', 'album')
            }),
    )

admin.site.register(SongFile, SongFileAdmin)
