from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateField


class User(AbstractUser):
    phone = CharField(max_length=20, blank=True)
    date_of_birth = DateField(null=True, blank=True)

    def __str__(self):
        return self.username
