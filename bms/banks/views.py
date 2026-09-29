"""Phase 3, approach A: APIView. You write everything by hand.

APIView is DRF's most manual view class. It gives you exactly three things
the plain Django View did not:

  1. request is a DRF Request  -> request.data, request.query_params
  2. authentication + permissions run before your method (stage 5b)
  3. exceptions become proper JSON error responses (stage 5e)

Everything else - which queryset, which serializer, pagination, filtering -
is yours to write. Compare with bms/banks/generic_views.py on the
phase3/generic branch, which declares the same endpoint in four lines.
"""

from django.db.models import Count
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bank
from .serializers import BankSerializer


class BankListAPIView(APIView):
    """GET /api/banks/ and POST /api/banks/

    Method routing happens in APIView.dispatch():
        handler = getattr(self, request.method.lower(), http_method_not_allowed)
    So defining get() and post() is all that "routing" means. A DELETE here
    returns 405 without you writing anything.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        banks = Bank.objects.annotate(branch_count=Count("branches")).order_by("name")
        serializer = BankSerializer(banks, many=True)
        
        return Response(serializer.data)

    def post(self, request):
       
        serializer = BankSerializer(data=request.data)

       
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BankDetailAPIView(APIView):
    """GET / PATCH / DELETE /api/banks/<pk>/

    Written out in full so you can see exactly how much
    RetrieveUpdateDestroyAPIView does for you in Phase 4.
    """

    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        """Fetch or 404.

        get_object_or_404 raises Http404, which DRF's exception handler
        converts into {"detail": "Not found."} with status 404. Using
        Bank.objects.get() directly would raise DoesNotExist and produce a
        500 instead.
        """
        from django.shortcuts import get_object_or_404

        return get_object_or_404(
            Bank.objects.annotate(branch_count=Count("branches")), pk=pk
        )

    def get(self, request, pk):
        return Response(BankSerializer(self.get_object(pk)).data)

    def patch(self, request, pk):
        serializer = BankSerializer(self.get_object(pk), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
