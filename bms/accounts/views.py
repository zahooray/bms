"""Phase 3, approach A: APIView for accounts.

The important difference from banks: accounts are PRIVATE. Every queryset in
this file is scoped to request.user. Get that wrong and one customer reads
another customer's balance.
"""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BankAccount
from .serializers import BankAccountSerializer


class AccountListAPIView(APIView):
    """GET /api/accounts/ and POST /api/accounts/ - the requesting user's only."""

    # Falls back to DEFAULT_PERMISSION_CLASSES = IsAuthenticated, but stating
    # it makes the intent obvious to the next reader.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """THE SECURITY BOUNDARY.

        filter(user=self.request.user) is the whole of this API's access
        control in Phase 3. Replace it with BankAccount.objects.all() and
        every user sees every account.

        select_related collapses what would otherwise be N+1: the serializer
        reads bank_branch.bank.name, bank_branch.name and user.username via
        `source`, and each of those is a query per row without this.
        """
        return (
            BankAccount.objects.filter(user=self.request.user)
            .select_related("user", "bank_branch", "bank_branch__bank")
            .order_by("-created")
        )

    def get(self, request):
        serializer = BankAccountSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # `user` is NOT a serializer field, so it cannot come from the body.
        # Injecting it here is what stops a client POSTing {"user": 7} and
        # creating an account owned by somebody else.
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailAPIView(APIView):
    """GET / PATCH / DELETE /api/accounts/<pk>/ - owner only."""

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, pk):
        """Scoping the LOOKUP, not just the list.

        Note the filter comes BEFORE the pk lookup. Asking for someone
        else's account id returns 404, not 403 - the row is simply not in
        the queryset this user can see.

        404-instead-of-403 is deliberate: a 403 would confirm the account
        exists, which leaks information.
        """
        return get_object_or_404(
            BankAccount.objects.filter(user=request.user).select_related(
                "user", "bank_branch__bank"
            ),
            pk=pk,
        )

    def get(self, request, pk):
        return Response(BankAccountSerializer(self.get_object(request, pk)).data)

    def patch(self, request, pk):
        serializer = BankAccountSerializer(
            self.get_object(request, pk), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
