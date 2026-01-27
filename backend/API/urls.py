from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ScheduleViewSet, ScheduleAPIView, LeaveViewSet, LeaveAPIView

router = SimpleRouter()
router.register(r"schedule", ScheduleViewSet, basename="schedule")
router.register(r"leave", LeaveViewSet, basename="leave")

urlpatterns = [
    path("", include(router.urls)),
    path("all-schedules/", ScheduleAPIView.as_view(), name="all-schedule"),
    path("all-leaves/", LeaveAPIView.as_view(), name="all-leave"),
]
