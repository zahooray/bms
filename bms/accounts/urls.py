from django.urls import path

from bms.accounts.views import AccountDetailView, AccountListView


app_name = "accounts"

urlpatterns = [
    path("", AccountListView.as_view(), name="list"),
    path("<int:pk>/", AccountDetailView.as_view(), name="detail"),
]
