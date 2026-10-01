from django.conf import settings
from django.db import models

from bms.core.models import BaseModel


class BankAccount(BaseModel):
    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    bank_branch = models.ForeignKey(
        "banks.BankBranch",
        on_delete=models.PROTECT,
        related_name="accounts",
    )
    account_number = models.CharField(max_length=34, unique=True)
    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.SAVINGS,
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.account_number} ({self.user.username})"
