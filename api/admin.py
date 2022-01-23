from django.contrib import admin
from .models import CarModel, CarBrand, UserCar

admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(UserCar)
