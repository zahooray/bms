from django.contrib import admin

from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number",
        "user",
        "bank_branch",
        "account_type",
        "balance",
        "is_active",
    )
    list_filter = ("account_type", "is_active", "bank_branch__bank")
    search_fields = ("account_number", "user__username", "user__email")
    list_select_related = ("user", "bank_branch")
    ordering = ("-created",)
    readonly_fields = ("created", "modified")
