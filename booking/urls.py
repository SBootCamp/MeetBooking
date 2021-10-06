from rest_framework.routers import DefaultRouter

from booking import views

router = DefaultRouter()
router.register("", views.CabinetView, basename="cabinets")
router.register("(?P<room_number>[^/.]+)/events", views.EventView, basename="events")
urlpatterns = router.urls
