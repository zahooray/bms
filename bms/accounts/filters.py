from django_filters import BooleanFilter, FilterSet, NumberFilter, OrderingFilter

from bms.accounts.models import Account


class AccountFilter(FilterSet):
    bank = NumberFilter(field_name="bank_branch__bank")
    is_islamic = BooleanFilter(field_name="bank_branch__bank__is_islamic")
    ordering = OrderingFilter(
        fields=(
            ("balance", "balance"),
            ("created", "created_at"),
            ("user__username", "username"),
        )
    )

    class Meta:
        model = Account
        fields = ["account_type"]
