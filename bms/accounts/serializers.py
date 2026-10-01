from decimal import Decimal

from rest_framework import serializers

from .models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    """A bank account, with bank/branch/owner names pulled in via `source`."""

    bank_name = serializers.CharField(source="bank_branch.bank.name", read_only=True)
    bank_is_islamic = serializers.BooleanField(source="bank_branch.bank.is_islamic", read_only=True)

    branch_name = serializers.CharField(source="bank_branch.name", read_only=True)
    owner = serializers.CharField(source="user.username", read_only=True)
    account_type_label = serializers.CharField(source="get_account_type_display", read_only=True)

    class Meta:
        model = BankAccount
        fields = [
            "id",
            "account_number",
            "account_type",
            "account_type_label",
            "balance",
            "bank_name",
            "bank_is_islamic",
            "branch_name",
            "owner",
            "bank_branch",
            "is_active",
            "created",
        ]

        read_only_fields = ["id", "is_active", "created"]

    def validate_balance(self, value):
        """Per-field. Runs only for `balance`."""
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Balance cannot be negative.")
        return value

    def validate_account_number(self, value):
        """Normalise, then check. Returning the transformed value is the point."""
        value = value.strip().upper()
        if not value.isalnum():
            raise serializers.ValidationError(
                "Account number must be alphanumeric, no spaces or symbols."
            )
        return value

    def validate(self, attrs):
        """Cross-field. Everything already passed its own validate_<field>().

        A savings account has a minimum opening balance; a current account
        does not. That rule needs BOTH fields, so it cannot live in either
        validate_account_type() or validate_balance().
        """
        account_type = attrs.get("account_type", BankAccount.AccountType.SAVINGS)
        balance = attrs.get("balance", Decimal("0.00"))

        if account_type == BankAccount.AccountType.SAVINGS and balance < Decimal("500.00"):
            raise serializers.ValidationError(
                {"balance": "A savings account requires an opening balance of at least 500."}
            )

        branch = attrs.get("bank_branch")
        if branch and not branch.is_active:
            raise serializers.ValidationError(
                {"bank_branch": "Cannot open an account at an inactive branch."}
            )
        return attrs
