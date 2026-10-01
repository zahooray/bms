from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from bms.accounts.models import BankAccount
from bms.accounts.serializers import BankAccountSerializer


class AccountScopedQuerysetMixin:
    def get_queryset(self):
        return (
            BankAccount.objects.filter(user=self.request.user)
            .select_related("user", "bank_branch", "bank_branch__bank")
            .order_by("-created")
        )


class AccountListView(AccountScopedQuerysetMixin, ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(AccountScopedQuerysetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]
