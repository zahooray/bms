from django.urls import path

from bms.accounts.views import AccountRetrieveUpdateDestroyAPIView, AccountListCreateAPIView


urlpatterns = [
    path("", AccountListCreateAPIView.as_view(), name="account-list"),
    path("<int:pk>/", AccountRetrieveUpdateDestroyAPIView.as_view(), name="account-detail"),
]
