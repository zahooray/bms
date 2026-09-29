from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("", views.AccountListAPIView.as_view(), name="list"),
    path("<int:pk>/", views.AccountDetailAPIView.as_view(), name="detail"),
]
