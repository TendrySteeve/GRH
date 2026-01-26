from rest_framework import serializers
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

    class Meta:
        model = models.Leave
        fields = [
            "id",
            "user",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "approved_by",
        ]
        read_only_fields = ["created_at"]
