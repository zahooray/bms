from django.urls import path

from bms.banks.views import BankDetailView, BankListView


app_name = "banks"

urlpatterns = [
    path("", BankListView.as_view(), name="list"),
    path("<int:pk>/", BankDetailView.as_view(), name="detail"),
]
