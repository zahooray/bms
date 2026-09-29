from django.contrib import admin

from .models import Bank, BankBranch


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("name", "swift_code", "is_islamic", "established_date", "is_active")
    list_filter = ("is_islamic", "is_active", "established_date")
    search_fields = ("name", "swift_code")
    ordering = ("name",)
    readonly_fields = ("created", "modified")


@admin.register(BankBranch)
class BankBranchAdmin(admin.ModelAdmin):
    list_display = ("name", "branch_code", "bank", "is_active")
    list_filter = ("bank", "is_active")
    search_fields = ("name", "branch_code", "bank__name")
    list_select_related = ("bank",)
    ordering = ("bank__name", "name")
    readonly_fields = ("created", "modified")
