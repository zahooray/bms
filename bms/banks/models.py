from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    TextField,
    UniqueConstraint,
)

from bms.core.models import BaseModel


class Bank(BaseModel):
    name = CharField(max_length=255, blank=True, null=True)
    swift_code = CharField(max_length=11, unique=True)
    is_islamic = BooleanField(default=False)
    established_date = DateField()

    def __str__(self):
        return f"{self.name} ({self.swift_code})"


class BankBranch(BaseModel):
    bank = ForeignKey(
        Bank,
        on_delete=CASCADE,
        related_name="branches",
    )
    name = CharField(max_length=255, null=True, blank=True)
    branch_code = CharField(max_length=255, null=True, blank=True)
    address = TextField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["bank", "branch_code"],
                name="unique_branch_code_per_bank",
            )
        ]

    def __str__(self):
        return f"{self.bank.name} - {self.name}"
