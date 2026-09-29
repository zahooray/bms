"""Phase 2 - plain Django views. No DRF anywhere in this file.

Everything here is done by hand on purpose. Phase 3 replaces most of it
with a serializer, and the contrast is the lesson.
"""

from django.db.models import Count
from django.http import JsonResponse
from django.views import View

from .models import Bank


class BankListView(View):
    """GET /banks/ -> every bank with its branch count.

    Subclasses django.views.View, which does exactly one thing: it looks at
    request.method and calls the matching method on this class.

        GET  -> self.get()
        POST -> self.post()   (not defined here, so POST returns 405)

    No templates, no forms, no DRF. Just method routing.
    """

    def get(self, request):
        # annotate() adds a computed column to EACH row. One SQL query with a
        # GROUP BY - not a Python loop calling .count() per bank (which would
        # be N+1).
        #
        # "branches" is the related_name on BankBranch.bank.
        banks = Bank.objects.annotate(branch_count=Count("branches")).order_by("name")

        # THE TEDIOUS PART. Model objects are not JSON, so every field is
        # copied into a dict by hand. In Phase 3 this whole block becomes:
        #     BankSerializer(banks, many=True).data
        data = [
            {
                "id": bank.id,
                "name": bank.name,
                "is_islamic": bank.is_islamic,
                # branch_count is NOT a model field. annotate() attached it
                # to each instance for this query only.
                "branch_count": bank.branch_count,
            }
            for bank in banks
        ]

        # JsonResponse wants a dict. Passing a bare list needs safe=False.
        # Wrapping in {"banks": [...]} also leaves room to add "count"/"next"
        # later, which is exactly what DRF pagination does in Phase 6.
        return JsonResponse({"count": len(data), "banks": data})
