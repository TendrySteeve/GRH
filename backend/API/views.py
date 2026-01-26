from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from . import serializers
from . import models


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            models.Schedule.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-date")
        )

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


class ScheduleAPIView(APIView):
    def get(self, request):
        schedules = models.Schedule.objects.all()
        serializer = serializers.ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LeaveSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ["ADMIN", "RH"]:
            return models.Leave.objects.select_related("user").order_by("-created_at")
        return models.Leave.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        leave = serializer.instance

        if "status" in serializer.validated_data:
            if user.role not in ["ADMIN", "RH"]:
                raise PermissionDenied("Vous n'êtes pas autorisé à valider un congé")

            serializer.save(approved_by=user)
            return

        if leave.user != user:
            raise PermissionDenied("Vous ne pouvez modifier que votre propre congé")

        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Vous ne pouvez supprimer que votre planning")
        instance.delete()
