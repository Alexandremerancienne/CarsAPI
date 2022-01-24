from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserCar, CarBrand, CarModel
from accounts.models import CustomUser
from .serializers import UserCarSerializer, CustomUserSerializer, CarBrandSerializer, CarModelSerializer
from .filters import CarFilter
from .permissions import IsSuperuserOrAdminOrCarUser, IsSuperuserOrAdmin, IsSuperuserOrSelfAdmin
from .exceptions import NotCarUser, NotUser


class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperuserOrSelfAdmin,
    )

    def list(self, request):
        queryset = CustomUser.objects.all().order_by("id")
        if self.request.user.role == "client":
            queryset = queryset.filter(id=request.user.id)
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        retrieved_user = get_object_or_404(CustomUser, id=pk)
        if self.request.user.role == "client" and retrieved_user != request.user:
            raise NotUser()
        serializer = CustomUserSerializer(retrieved_user)
        return Response(serializer.data)


class CarViewSet(viewsets.ModelViewSet):

    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperuserOrAdminOrCarUser,
    )

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CarFilter

    def list(self, request):
        queryset = UserCar.objects.all().order_by("id")
        if self.request.user.role == "client":
            queryset = queryset.filter(user=request.user)

        serializer = UserCarSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        retrieved_car = get_object_or_404(UserCar, id=pk)
        if self.request.user.role == "client" and retrieved_car.user != request.user:
            raise NotCarUser()

        serializer = UserCarSerializer(retrieved_car)
        return Response(serializer.data)


class CarBrandViewSet(viewsets.ModelViewSet):

    queryset = CarBrand.objects.all()
    serializer_class = CarBrandSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperuserOrAdmin,
    )

    def destroy(self, request, pk=None):
        brand = get_object_or_404(CarBrand, id=pk)
        queryset = CarModel.objects.all().filter(car_brand=brand)
        for model in queryset:
            self.check_object_permissions(request, model)
            self.perform_destroy(model)
        self.perform_destroy(brand)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarModelViewSet(viewsets.ModelViewSet):

    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperuserOrAdmin,
    )

