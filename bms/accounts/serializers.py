from decimal import Decimal

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)
from rest_framework.validators import UniqueValidator

from bms.accounts.constants import AccountType
from bms.accounts.models import BankAccount
from bms.banks.models import BankBranch
from bms.banks.serializers import BankBranchNestedSerializer
from bms.core.serializer_fields import UpperCaseCharField


class BankAccountSerializer(ModelSerializer):
    branch = BankBranchNestedSerializer(source="bank_branch", read_only=True)
    bank_branch = PrimaryKeyRelatedField(queryset=BankBranch.objects.all(), write_only=True)
    owner = CharField(source="user.username", read_only=True)
    account_type_label = CharField(source="get_account_type_display", read_only=True)
    account_number = UpperCaseCharField(
        max_length=34,
        validators=[UniqueValidator(queryset=BankAccount.objects.all())],
    )

    class Meta:
        model = BankAccount
        fields = [
            "id",
            "account_number",
            "account_type",
            "account_type_label",
            "balance",
            "branch",
            "owner",
            "bank_branch",
            "is_active",
            "created",
        ]
        read_only_fields = ["id", "is_active", "created"]

    def validate_balance(self, value):
        if value < Decimal("0.00"):
            raise ValidationError("Balance cannot be negative.")
        return value

    def validate_account_number(self, value):
        if not value.isalnum():
            raise ValidationError("Account number must be alphanumeric, no spaces or symbols.")
        return value

    def validate(self, attrs):
        account_type = attrs.get("account_type", AccountType.SAVINGS)
        balance = attrs.get("balance", Decimal("0.00"))

        if account_type == AccountType.SAVINGS and balance < Decimal("500.00"):
            raise ValidationError(
                {"balance": "A savings account requires an opening balance of at least 500."}
            )

        branch = attrs.get("bank_branch")
        if branch and not branch.is_active:
            raise ValidationError({"bank_branch": "Cannot open an account at an inactive branch."})
        return attrs
