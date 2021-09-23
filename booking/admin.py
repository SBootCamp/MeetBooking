from django.contrib import admin
from .models import *

admin.site.register(Cabinet)
admin.site.register(Event)
admin.site.register(DateBooking)
admin.site.register(TimeBooking)

