from rest_framework.serializers import CharField


class UpperCaseCharField(CharField):
    def to_internal_value(self, data):
        return super().to_internal_value(data).strip().upper()
