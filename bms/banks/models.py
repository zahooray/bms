from django.db import models

from bms.core.models import BaseModel


class Bank(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    swift_code = models.CharField(max_length=11, unique=True)
    is_islamic = models.BooleanField(default=False)
    established_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.swift_code})"


class BankBranch(BaseModel):
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name="branches",
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    branch_code = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bank", "branch_code"],
                name="unique_branch_code_per_bank",
            )
        ]

    def __str__(self):
        return f"{self.bank.name} - {self.name}"
