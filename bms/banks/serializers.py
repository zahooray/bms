from django.utils.timezone import localdate
from rest_framework.serializers import IntegerField, ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

from bms.banks.models import Bank, BankBranch
from bms.core.serializer_fields import UpperCaseCharField


class BankNestedSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = ["id", "name", "swift_code", "is_islamic"]


class BankBranchNestedSerializer(ModelSerializer):
    bank = BankNestedSerializer(read_only=True)

    class Meta:
        model = BankBranch
        fields = ["id", "name", "branch_code", "bank"]


class BankSerializer(ModelSerializer):
    branch_count = IntegerField(read_only=True)
    swift_code = UpperCaseCharField(
        max_length=11,
        validators=[UniqueValidator(queryset=Bank.objects.all())],
    )

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

    def validate_swift_code(self, value):
        if len(value) not in (8, 11):
            raise ValidationError("SWIFT/BIC must be 8 or 11 characters.")
        return value

    def validate(self, attrs):
        established = attrs.get("established_date")
        if established and established > localdate():
            raise ValidationError({"established_date": "Established date cannot be in the future."})
        return attrs


class BankBranchSerializer(ModelSerializer):
    bank_detail = BankNestedSerializer(source="bank", read_only=True)

    class Meta:
        model = BankBranch
        fields = [
            "id",
            "bank",
            "bank_detail",
            "name",
            "branch_code",
            "address",
            "is_active",
        ]
        read_only_fields = ["id", "is_active"]
