from rest_framework.serializers import CharField, Serializer


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField(write_only=True, style={"input_type": "password"})
