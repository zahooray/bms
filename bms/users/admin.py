from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from bms.users.models import User


@register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "phone", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "phone")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional info", {"fields": ("phone", "date_of_birth")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("phone", "date_of_birth")}),
    )
