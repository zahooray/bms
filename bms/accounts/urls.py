from django.urls import path

from bms.accounts.views import (
    AccountBalanceUpdateAPIView,
    AccountListCreateAPIView,
    AccountRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    path("", AccountListCreateAPIView.as_view(), name="account-list"),
    path("<int:pk>/", AccountRetrieveUpdateDestroyAPIView.as_view(), name="account-detail"),
    path("<int:pk>/balance/", AccountBalanceUpdateAPIView.as_view(), name="account-balance"),
]
