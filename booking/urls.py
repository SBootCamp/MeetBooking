from django.urls import path

from . import views

urlpatterns = [
    path('', views.CabinetListView.as_view(), name='cabinet-list'),
    path('detail/<int:pk>/', views.CabinetDetailView.as_view(), name='cabinet-detail'),
    path('booking/', views.BookingView.as_view(), name='booking'),
]