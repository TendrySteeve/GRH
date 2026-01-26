from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ScheduleViewSet, ScheduleAPIView

router = SimpleRouter()
router.register(
    r'schedule',
    ScheduleViewSet,
    basename='schedule'
)

urlpatterns = [
    path('', include(router.urls)),
    path('all-schedules/', ScheduleAPIView.as_view(), name="all-schedule")
]
