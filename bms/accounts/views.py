from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from bms.accounts.models import Account
from bms.accounts.serializers import (
    AccountBalanceSerializer,
    AccountCreateUpdateSerializer,
    AccountSerializer,
)
from bms.core.permissions import IsOwnerOrStaff


class AccountListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return AccountCreateUpdateSerializer
        return AccountSerializer

    def get_queryset(self):
        return (
            Account.objects.filter(user=self.request.user)
            .select_related("user", "bank_branch", "bank_branch__bank")
            .order_by("-created")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Account.objects.select_related("user", "bank_branch", "bank_branch__bank")

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return AccountCreateUpdateSerializer
        return AccountSerializer


class AccountBalanceUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    serializer_class = AccountBalanceSerializer
    queryset = Account.objects.select_related("user")
    http_method_names = ["patch"]
