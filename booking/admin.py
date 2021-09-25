from django.contrib import admin
from .models import *


@admin.register(Event)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'cabinet', 'date', 'start_time', 'end_time')


admin.site.register(Cabinet)
