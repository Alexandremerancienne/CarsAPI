from rest_framework import serializers
from .models import UserCar, CarModel, CarBrand
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "role")


class UserCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCar
        fields = ("id", "user", "car_brand", "car_model", "odo")


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ("name",)


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ("car_brand", "name")
