from django.contrib import admin
from .models import Cabinet, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'cabinet', 'start_time', 'end_time')


admin.site.register(Cabinet)
