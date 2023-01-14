from django.urls import reverse
from rest_framework import status


class AuthTokenMixin:
    login_url = reverse("rest_login")

    def get_token(self, user):
        data = {
            "email": user.email,
            "password": "password",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data.get("key")
