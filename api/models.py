from django.conf import settings
from django.db import models


class CarBrand(models.Model):
    class Meta:
        verbose_name_plural = "Brands"

    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name.upper()}"


class CarModel(models.Model):
    class Meta:
        verbose_name_plural = "Models"

    car_brand = models.ForeignKey(to=CarBrand, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_brand} {self.name}"


class UserCar(models.Model):
    class Meta:
        verbose_name_plural = "Cars"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    car_brand = models.ForeignKey(to=CarBrand, null=True, on_delete=models.SET_NULL)
    car_model = models.ForeignKey(to=CarModel, null=True, on_delete=models.SET_NULL)
    first_reg = models.DateTimeField(auto_now_add=True)
    odo = models.IntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_model} - {self.user.username}"
