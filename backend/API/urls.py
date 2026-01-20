from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WeeklyScheduleViewSet

router = SimpleRouter()
router.register(
    r'schedule',
    WeeklyScheduleViewSet,
    basename='schedule'
)

urlpatterns = [
    path('', include(router.urls)),
]
