from django.urls import path

from . import views

urlpatterns = [
    path('booking/room/<int:pk>', views.BookingView.as_view(), name='booking'),
]