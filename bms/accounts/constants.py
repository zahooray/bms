from django.db.models import TextChoices


class AccountType(TextChoices):
    SAVINGS = "savings", "Savings"
    CURRENT = "current", "Current"


class TransactionType(TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"
