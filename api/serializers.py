from rest_framework import serializers
from .models import UserCar, CarModel, CarBrand
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "role", "password", "location")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
            "location": {"write_only": True},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCar
        fields = (
            "id",
            "user",
            "car_brand",
            "car_model",
            "odo",
        )


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = (
            "id",
            "name",
        )


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ("id", "car_brand", "name")
