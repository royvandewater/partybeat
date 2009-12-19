from django.contrib import admin
from xmms2_django.song_storage.models import *

class SongFileAdmin(admin.ModelAdmin):
    list_display = ('artist', 'album', 'name',) # The future listview

admin.site.register(SongFile, SongFileAdmin)
