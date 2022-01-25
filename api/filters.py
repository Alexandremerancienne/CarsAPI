from django_filters import rest_framework as filters
from api.models import UserCar, CarModel, CarBrand


class ModelFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="iexact")
    name_contains = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = CarModel
        fields = [
            "name",
            "name_contains",
        ]


class BrandFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="iexact")
    name_contains = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = CarBrand
        fields = [
            "name",
            "name_contains",
        ]


class CarFilter(filters.FilterSet):

    odo_gte = filters.NumberFilter(field_name="odo", lookup_expr="gte")
    odo_lte = filters.NumberFilter(field_name="odo", lookup_expr="lte")
    brand = filters.CharFilter(field_name="car_brand", lookup_expr="name__iexact")
    brand__contains = filters.CharFilter(
        field_name="car_brand", lookup_expr="name__icontains"
    )
    model = filters.CharFilter(field_name="car_model", lookup_expr="name__iexact")
    model__contains = filters.CharFilter(
        field_name="car_model", lookup_expr="name__icontains"
    )
    sort_by = filters.CharFilter(method="filter_sort_by", label="Sort by")

    def filter_sort_by(self, queryset, _, value):
        values = value.lower().split(",")
        return queryset.order_by(*values)

    class Meta:
        model = UserCar
        fields = [
            "brand",
            "car_brand",
            "brand__contains",
            "model",
            "car_model",
            "model__contains",
            "sort_by",
            "odo_gte",
            "odo_lte",
        ]
