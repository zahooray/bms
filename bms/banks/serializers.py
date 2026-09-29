from django.utils import timezone
from rest_framework import serializers

from .models import Bank, BankBranch


class BankSerializer(serializers.ModelSerializer):
    branch_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bank
        fields = [
            "id",
            "name",
            "swift_code",
            "is_islamic",
            "established_date",
            "branch_count",
            "is_active",
        ]
        read_only_fields = ["id", "is_active"]

    def to_internal_value(self, data):

        if isinstance(data, dict) and data.get("swift_code"):
            data = data.copy()
            data["swift_code"] = data["swift_code"].strip().upper()
        return super().to_internal_value(data)

    def validate_swift_code(self, value):
        if len(value) not in (8, 11):
            raise serializers.ValidationError("SWIFT/BIC must be 8 or 11 characters.")
        return value

    def validate(self, attrs):
        established = attrs.get("established_date")
        if established:
            if established > timezone.localdate():
                raise serializers.ValidationError(
                    {"established_date": "Established date cannot be in the future."}
                )
        return attrs


class BankBranchSerializer(serializers.ModelSerializer):
    """Branch, with a couple of fields reached through the FK via `source`."""

    bank_name = serializers.CharField(source="bank.name", read_only=True)
    bank_is_islamic = serializers.BooleanField(source="bank.is_islamic", read_only=True)

    class Meta:
        model = BankBranch
        fields = [
            "id",
            "bank",
            "bank_name",
            "bank_is_islamic",
            "name",
            "branch_code",
            "address",
            "is_active",
        ]
        read_only_fields = ["id", "is_active"]
