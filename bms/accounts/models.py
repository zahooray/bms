from django.db.models import CASCADE, CharField, DateField, DecimalField, ForeignKey

from bms.accounts.constants import AccountType, TransactionType
from bms.core.models import BaseModel


class Account(BaseModel):
    account_number = CharField(max_length=34, unique=True)
    account_type = CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.SAVINGS,
    )
    balance = DecimalField(max_digits=12, decimal_places=2, default=0)

    user = ForeignKey(
        "users.User",
        on_delete=CASCADE,
        related_name="accounts",
    )
    bank_branch = ForeignKey(
        "banks.Branch",
        on_delete=CASCADE,
        related_name="accounts",
    )

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"
        db_table = "accounts"

    def __str__(self):
        return f"{self.account_number} ({self.user.username})"


class Transaction(BaseModel):
    type = CharField(max_length=10, choices=TransactionType.choices)
    date = DateField()
    amount = DecimalField(max_digits=12, decimal_places=2)
    account = ForeignKey(
        Account,
        on_delete=CASCADE,
        related_name="transactions",
    )

    class Meta:
        verbose_name = "transaction"
        verbose_name_plural = "transactions"
        db_table = "transactions"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.get_type_display()} of {self.amount} on {self.date}"
