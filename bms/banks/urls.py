from django.urls import path

from . import views

app_name = "banks"

urlpatterns = [
  path("", views.BankListView.as_view(), name="list"),
  path("<int:pk>/", views.BankDetailView.as_view(), name="detail"),
]
