from django.contrib import admin

from models import *

class XmmsStatusAdmin(admin.ModelAdmin):
    list_display = ('last_update', 'current_action', 'timeout', 'playlist_size', 'current_position')
    # fields = ['play_mode','timeout']
    fieldsets = [
        (None,              {'fields':  ['play_mode', 'timeout']}),
        ('Current Status',  {'fields':  ['current_action', 'last_update', 'playlist_size',
                                         'current_position', 'seek', 'max_seek', 'volume'],
                             'classes': ['collapse']}),
    ]

class ActionAdmin(admin.ModelAdmin):
    list_display = ('command',)

admin.site.register(XmmsStatus, XmmsStatusAdmin)
admin.site.register(Action, ActionAdmin)
