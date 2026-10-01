from django.db.models import Count
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from bms.banks.models import Bank
from bms.banks.serializers import BankSerializer


class BankListView(ListCreateAPIView):
    queryset = Bank.objects.annotate(branch_count=Count("branches")).order_by("name")
    serializer_class = BankSerializer
    permission_classes = [AllowAny]


class BankDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.annotate(branch_count=Count("branches"))
    serializer_class = BankSerializer
    permission_classes = [AllowAny]

    def perform_destroy(self, instance):
        if instance.branches.filter(accounts__isnull=False).exists():
            raise ValidationError(
                {"detail": "Cannot delete a bank whose branches still hold accounts."}
            )
        instance.delete()
