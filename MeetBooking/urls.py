import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from MeetBooking.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('cabinets/', include('booking.urls')),
]
if DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('frontend/', include('frontend.urls'))
    ]
