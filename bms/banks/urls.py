from django.urls import path

from bms.banks.views import BankRetrieveUpdateDestroyAPIView, BankListCreateAPIView


urlpatterns = [
    path("", BankListCreateAPIView.as_view(), name="bank-list"),
    path("<int:pk>/", BankRetrieveUpdateDestroyAPIView.as_view(), name="bank-detail"),
]
