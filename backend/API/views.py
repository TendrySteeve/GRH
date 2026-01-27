from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone


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

        if user.role in ["ADMIN", "RESP"]:
            return models.Leave.objects.select_related("user", "approved_by").order_by(
                "-created_at"
            )

        return models.Leave.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        leave = serializer.instance

        if "status" in serializer.validated_data:
            if user.role not in ["ADMIN", "RESP"]:
                raise PermissionDenied(
                    "Seul l'ADMIN ou le RESPONSABLE peut valider/rejeter un congé."
                )
            serializer.save(approved_by=user, approved_at=timezone.now())
            return

        if leave.user != user:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres congés.")

        if leave.status in ["APPROVED", "REJECTED"]:
            raise PermissionDenied(
                "Un congé validé ou rejeté ne peut plus être modifié."
            )

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if instance.user == user and instance.status in ["PENDING"]:
            instance.delete()
            return

        if user.role in ["ADMIN", "RESP"]:
            instance.delete()
            return

        raise PermissionDenied(
            "Vous ne pouvez pas supprimer un congé validé ou rejeté."
        )
