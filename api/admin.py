from django.contrib import admin
from .models import CarModel, CarBrand, UserCar


class SoftDeleteAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()


class CarModelAdmin(SoftDeleteAdmin):
    model = CarModel
    list_filter = ("name", "deleted_at")


class CarBrandAdmin(SoftDeleteAdmin):
    model = CarModel
    list_filter = ("name", "deleted_at")


class UserCarAdmin(SoftDeleteAdmin):
    model = CarModel
    list_filter = ("user", "car_brand", "car_model", "deleted_at")


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(UserCar, UserCarAdmin)
