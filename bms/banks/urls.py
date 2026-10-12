from django.urls import path

from bms.banks.views import BankListCreateAPIView, BankRetrieveUpdateDestroyAPIView


urlpatterns = [
    path("", BankListCreateAPIView.as_view(), name="bank-list"),
    path("<int:pk>/", BankRetrieveUpdateDestroyAPIView.as_view(), name="bank-detail"),
]
