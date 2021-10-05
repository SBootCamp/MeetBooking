from rest_framework.routers import DefaultRouter

from booking import views

router = DefaultRouter()
router.register("", views.CabinetViewSet, basename="cabinets")
router.register("(?P<room_number>[^/.]+)/events", views.EventViewSet, basename="events")
urlpatterns = router.urls
