from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import WeeklyScheduleSerializer
from .models import WeeklySchedule


class WeeklyScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklyScheduleSerializer

    def get_queryset(self):
        return WeeklySchedule.objects.select_related("user")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Vous ne pouvez modifier que votre planning")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Vous ne pouvez supprimer que votre planning")
        instance.delete()
