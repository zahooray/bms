from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy


class LoginView(DjangoLoginView):
    redirect_authenticated_user = True


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy("users:login")
