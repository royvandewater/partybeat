from django.contrib import admin

from models import *

class XmmsStatusAdmin(admin.ModelAdmin):
    list_display = ('last_update', 'current_action', 'timeout')

class ActionAdmin(admin.ModelAdmin):
    list_display = ('command',)

admin.site.register(XmmsStatus, XmmsStatusAdmin)
admin.site.register(Action, ActionAdmin)
