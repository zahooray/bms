from django.db.models import TextChoices


class AccountType(TextChoices):
    SAVINGS = "savings", "Savings"
    CURRENT = "current", "Current"
