from django.urls import path
from rest_framework.routers import DefaultRouter

from booking.api.views import CabinetViewSet, EventViewSet
from booking.views import CabinetDetailView

router = DefaultRouter()
router.register("api/cabinets", CabinetViewSet, basename="cabinets")
router.register("api/cabinets/(?P<room_number>[^/.]+)/events", EventViewSet, basename="events")
urlpatterns = router.urls

urlpatterns += [
    path("cabinets/<int:pk>/", CabinetDetailView.as_view(), name="booking")
]
