<<<<<<< HEAD
from django.contrib import admin
from .models import *
=======
>>>>>>> 94ac9410c4f8561469fa2e80b344138db6038bc4


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'cabinet', 'start_time', 'end_time')


admin.site.register(Cabinet)
