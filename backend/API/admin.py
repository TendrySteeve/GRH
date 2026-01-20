from django.contrib import admin

from . import models
@admin.register(models.WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
  pass