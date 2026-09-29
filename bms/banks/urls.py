from django.urls import path

from . import views


app_name = "banks"

urlpatterns = [
    path("", views.BankListAPIView.as_view(), name="list"),
    # <int:pk> casts the captured segment to a real int before it reaches
    # the view. Without the converter it would arrive as the string "5".
    path("<int:pk>/", views.BankDetailAPIView.as_view(), name="detail"),
]
