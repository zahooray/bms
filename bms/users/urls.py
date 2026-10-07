from django.urls import path

from bms.users.views import UserLoginAPIView, UserLogoutAPIView


urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("logout/", UserLogoutAPIView.as_view(), name="user-logout"),
]
