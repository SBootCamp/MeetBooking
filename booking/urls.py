from django.urls import path
from rest_framework.routers import DefaultRouter

from booking import api_views, views

router = DefaultRouter()
router.register("api/cabinets", api_views.CabinetViewSet, basename="cabinets")
router.register("api/cabinets/(?P<room_number>[^/.]+)/events", api_views.EventViewSet, basename="events")
urlpatterns = router.urls

urlpatterns += [
    path("cabinets/<int:pk>/booking", views.BookingView.as_view(), name="booking")
]
