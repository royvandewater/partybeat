from django.contrib import admin

from models import *

class XmmsStatusAdmin(admin.ModelAdmin):
    list_display = ('last_update', 'current_action',)

admin.site.register(XmmsStatus, XmmsStatusAdmin)
