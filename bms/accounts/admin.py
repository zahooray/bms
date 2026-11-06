from django.contrib.admin import ModelAdmin, register

from bms.accounts.models import Account, Transaction


@register(Account)
class AccountAdmin(ModelAdmin):
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


@register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ("account", "type", "amount", "date", "is_active")
    list_filter = ("type", "is_active", "account__bank_branch__bank")
    search_fields = ("account__account_number", "account__user__username")
    list_select_related = ("account__user",)
    autocomplete_fields = ("account",)
    date_hierarchy = "date"
    readonly_fields = ("created", "modified")
