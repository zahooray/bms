from decimal import Decimal

from rest_framework.serializers import CharField, ModelSerializer, ValidationError

from bms.accounts.constants import AccountType
from bms.accounts.models import Account
from bms.banks.serializers import BranchSerializer
from bms.core.serializer_fields import UpperCaseCharField


class AccountSerializer(ModelSerializer):
  bank_branch = BranchSerializer(read_only=True)
  username = CharField(source="user.username", read_only=True)
  account_type_label = CharField(source="get_account_type_display", read_only=True)
  
  class Meta:
    model = Account
    fields = "__all__"


class AccountCreateUpdateSerializer(ModelSerializer):
  account_number = UpperCaseCharField(max_length=34)
  
  class Meta:
    model = Account
    fields = "__all__"
    read_only_fields = ["id", "is_active", "created", "user"]
  
  def validate_balance(self, value):
    if value < Decimal("0.00"):
      raise ValidationError("Balance cannot be negative.")
    return value
  
  def validate_account_number(self, value):
    if not value.isalnum():
      raise ValidationError("Account number must be alphanumeric, no spaces or symbols.")
    
    accounts = Account.objects.filter(account_number=value)
    if self.instance:
      accounts = accounts.exclude(id=self.instance.id)
    if accounts.exists():
      raise ValidationError("An account with this number already exists.")
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
