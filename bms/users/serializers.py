from django.contrib.auth import authenticate
from rest_framework.serializers import CharField, Serializer, ValidationError


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        user = authenticate(
            request=self.context["request"],
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise ValidationError("Invalid username or password.")
        attrs["user"] = user
        return attrs
