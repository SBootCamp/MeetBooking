from django.urls import path

from . import views

urlpatterns = [
    path('', views.CabinetListView.as_view(), name='cabinet_list'),
    path('booking/<int:pk>', views.BookingView.as_view(), name='booking'),
]