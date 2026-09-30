"""Banks API - generic views.

Every endpoint here is CRUD over a model, so each one declares a queryset
and a serializer and lets DRF supply the rest: pagination, filter backends,
404 handling and object-level permissions.

The hand-written APIView versions were deleted; they are still readable in
git history if you want to compare.
"""

from django.db.models import Count
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Bank
from .serializers import BankSerializer


class BankListView(ListCreateAPIView):

    queryset = Bank.objects.annotate(branch_count=Count("branches")).order_by("name")
    serializer_class = BankSerializer
    permission_classes = [permissions.AllowAny]


class BankDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Bank.objects.annotate(branch_count=Count("branches"))
    serializer_class = BankSerializer
    permission_classes = [permissions.AllowAny]

    def perform_destroy(self, instance):
        
        if instance.branches.filter(accounts__isnull=False).exists():
            raise ValidationError(
                {"detail": "Cannot delete a bank whose branches still hold accounts."}
            )
        instance.delete()
