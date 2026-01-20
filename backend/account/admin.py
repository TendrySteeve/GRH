from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "role")

admin.site.register(User, UserAdmin)