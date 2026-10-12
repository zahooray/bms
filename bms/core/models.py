from django.db import models
from django.db.models import Transform
from django.db.models.fields import Field
from django.utils import timezone


class classproperty(property):
    def __get__(self, owner_self, owner_cls) -> models.Manager:
        return self.fget(owner_cls)


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    @classproperty
    def active_objects(cls) -> models.Manager:
        return cls.objects.filter(is_active=True)

    class Meta:
        abstract = True


@Field.register_lookup
class IntegerValue(Transform):
    lookup_name = "int"
    bilateral = True

    def as_sql(self, compiler, connection, **extra_context):
        sql, params = compiler.compile(self.lhs)
        sql = "CAST(%s AS DOUBLE PRECISION)" % sql
        return sql, params
