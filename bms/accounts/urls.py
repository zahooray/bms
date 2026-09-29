from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.AccountListView.as_view(), name="list"),
    # The function-based twin, so you can hit both and compare:
    path("fbv/", views.account_list_fbv, name="list-fbv"),
]
