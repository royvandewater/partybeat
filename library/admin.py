from django.contrib import admin
from models import *

class SongFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'album', 'artist',) # The future listview
    search_fields = ['name', 'album', 'artist'] # Search fields
    fieldsets = (
            (None, {
                'fields': ('file',)
            }),
            ('Leave blank to extract from id3', {
                'fields': ('name', 'artist', 'album')
            }),
    )

admin.site.register(SongFile, SongFileAdmin)
