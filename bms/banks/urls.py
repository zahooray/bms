from django.urls import path

from bms.banks.views import BankDetailView, BankListView


urlpatterns = [
    path("", BankListView.as_view(), name="bank-list"),
    path("<int:pk>/", BankDetailView.as_view(), name="bank-detail"),
]
