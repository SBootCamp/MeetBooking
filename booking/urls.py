from django.urls import path
from rest_framework.routers import DefaultRouter

from booking import views

router = DefaultRouter()
router.register("", views.CabinetView, basename="cabinets")
router.register("(?P<room_number>[^/.]+)/event", views.EventView, basename="event")
urlpatterns = router.urls





