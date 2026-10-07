from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    TextField,
)

from bms.core.models import BaseModel


class Bank(BaseModel):
  name = CharField(max_length=255, blank=True, null=True)
  swift_code = CharField(max_length=11, unique=True)
  is_islamic = BooleanField(default=False)
  established_date = DateField()
  
  class Meta:
    verbose_name = "bank"
    verbose_name_plural = "banks"
    db_table = "banks"
    unique_together = ["bank", "branch_code"]
  
  def __str__(self):
    return f"{self.name} ({self.swift_code})"


class Branch(BaseModel):
  name = CharField(max_length=255, null=True, blank=True)
  branch_code = CharField(max_length=255, null=True, blank=True)
  address = TextField()
  
  bank = ForeignKey(
    'banks.Bank',
    on_delete=CASCADE,
    related_name="branches",
  )
  
  class Meta:
    verbose_name = "branch"
    verbose_name_plural = "branches"
    db_table = "branches"
  
  def __str__(self):
    return f"{self.bank.name} - {self.name}"
