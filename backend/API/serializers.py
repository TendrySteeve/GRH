from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

from . import models


class ScheduleSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = models.Schedule
        fields = [
            "id",
            "user",
            "date",
            "status",
            "status_label",
            "description",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class LeaveSerializer(serializers.ModelSerializer):
    leave_type_label = serializers.CharField(
        source="get_leave_type_display", read_only=True
    )
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = models.Leave
        fields = [
            "id",
            "user",
            "user_name",
            "leave_type",
            "leave_type_label",
            "start_date",
            "end_date",
            "reason",
            "status",
            "status_label",
            "approved_by",
            "approved_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "user",
            "approved_by",
            "approved_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        request_user = self.context["request"].user
        validated_data["user"] = request_user
        return super().create(validated_data)

    # -----------------------
    # Mise à jour
    # -----------------------
    def update(self, instance, validated_data):
        request_user = self.context["request"].user

        # 🟢 Validation par ADMIN ou RESP
        if "status" in validated_data:
            if request_user.role not in ["ADMIN", "RESP"]:
                raise PermissionDenied(
                    "Seul l'ADMIN ou le RESPONSABLE peut valider un congé."
                )

            instance.approved_by = request_user
            instance.approved_at = timezone.now()

        return super().update(instance, validated_data)

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        if user.role == "EMPLOYEE" and "status" in data:
            raise PermissionDenied(
                "Vous n'êtes pas autorisé à valider ou rejeter un congé."
            )

        start_date = data.get("start_date", getattr(self.instance, "start_date", None))
        end_date = data.get("end_date", getattr(self.instance, "end_date", None))

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "La date de début doit être antérieure à la date de fin."
            )

        if self.instance and self.instance.status == "APPROVED":
            raise serializers.ValidationError(
                "Un congé déjà approuvé ne peut plus être modifié."
            )

        return data
