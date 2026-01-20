from rest_framework import serializers
from .models import WeeklySchedule


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = WeeklySchedule
        fields = [
            "id",
            "user",
            "date",
            "start_time",
            "end_time",
            "status",
            "status_label",
            "description",
            "created_at",
        ]
        read_only_fields = ["created_at"]
