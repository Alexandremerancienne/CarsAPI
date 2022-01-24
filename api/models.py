import datetime
from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from datetime import timezone


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive = kwargs.pop("alive", True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive:
            return SoftDeleteQuerySet(self.model).filter(deleted_at=None)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        now = datetime.datetime.now()
        return super(SoftDeleteQuerySet, self).update(deleted_at=now)

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive=False)

    class Meta:
        abstract = True

    def delete(self):
        now = datetime.datetime.now()
        self.deleted_at = now
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()


class CarBrand(SoftDeleteModel):
    class Meta:
        verbose_name_plural = "Brands"

    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name.upper()}"

class CarModelManager(models.Manager):
    def get_queryset(self):
        return (
            super(CarModelManager, self)
            .get_queryset()
            .filter(car_brand__deleted_at__isnull=True)
        )


class CarModel(SoftDeleteModel):

    objects = CarModelManager()

    class Meta:
        verbose_name_plural = "Models"

    car_brand = models.ForeignKey(to=CarBrand, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_brand} {self.name}"


class UserCar(SoftDeleteModel):

    class Meta:
        verbose_name_plural = "Cars"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )
    car_brand = models.ForeignKey(to=CarBrand, null=True, on_delete=models.SET_NULL)
    car_model = models.ForeignKey(to=CarModel, null=True, on_delete=models.SET_NULL)
    first_reg = models.DateTimeField(auto_now_add=True)
    odo = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_model} - {self.user.username}"
