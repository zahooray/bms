from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from bms.accounts.models import Account
from bms.accounts.serializers import AccountCreateUpdateSerializer, AccountSerializer


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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT", "PATCH"):
            return AccountCreateUpdateSerializer
        return AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user).select_related(
            "user", "bank_branch", "bank_branch__bank"
        )
