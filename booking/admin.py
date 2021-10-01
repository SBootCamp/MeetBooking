from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'cabinet', 'start_time', 'end_time')
    list_filter = ('cabinet',)


admin.site.register(Cabinet)
