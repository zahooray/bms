from django.utils.timezone import localdate
from rest_framework.serializers import IntegerField, ModelSerializer, ValidationError

from bms.banks.models import Bank, Branch
from bms.core.serializer_fields import UpperCaseCharField


class BankSerializer(ModelSerializer):
  branch_count = IntegerField(read_only=True)
  swift_code = UpperCaseCharField(max_length=11)
  
  class Meta:
    model = Bank
    fields = "__all__"
    read_only_fields = ["id", "is_active", "created"]
  
  def validate_swift_code(self, value):
    if len(value) not in (8, 11):
      raise ValidationError("SWIFT/BIC must be 8 or 11 characters.")
    
    banks = Bank.objects.filter(swift_code=value)
    if self.instance:
      banks = banks.exclude(id=self.instance.id)
    if banks.exists():
      raise ValidationError("A bank with this SWIFT code already exists.")
    return value
  
  def validate(self, attrs):
    established = attrs.get("established_date")
    if established and established > localdate():
      raise ValidationError({"established_date": "Established date cannot be in the future."})
    return attrs


class BranchSerializer(ModelSerializer):
  bank = BankSerializer(read_only=True)
  
  class Meta:
    model = Branch
    fields = "__all__"
