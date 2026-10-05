from django.conf import settings
from django.db.models import CASCADE, CharField, DecimalField, ForeignKey

from bms.accounts.constants import AccountType
from bms.core.models import BaseModel


class BankAccount(BaseModel):
    account_number = CharField(max_length=34, unique=True)
    account_type = CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.SAVINGS,
    )
    balance = DecimalField(max_digits=12, decimal_places=2, default=0)

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="accounts",
    )
    bank_branch = ForeignKey(
        "banks.BankBranch",
        on_delete=CASCADE,
        related_name="accounts",
    )

    def __str__(self):
        return f"{self.account_number} ({self.user.username})"
