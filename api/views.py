from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserCar, CarBrand, CarModel
from accounts.models import CustomUser
from .serializers import (
    UserCarSerializer,
    CustomUserSerializer,
    CarBrandSerializer,
    CarModelSerializer,
    ChangePasswordSerializer,
)
from .filters import CarFilter
from .permissions import (
    IsSuperuserOrAdminOrCarUser,
    IsSuperuserOrAdmin,
    IsSuperuserOrSelfAdminOrAnonymousUser,
)
from .exceptions import (
    NotCarUser,
    NotUser,
    NoPairBrandModel,
    CannotCreateOrEditCarForSuperUserOrAnotherAdmin,
    CannotCreateCarForAnotherUser,
)


from rest_framework import generics


class CustomUserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (
        IsAuthenticated,
        IsSuperuserOrSelfAdminOrAnonymousUser,
    )

    def list(self, request):
        queryset = CustomUser.objects.all().order_by("id")
        if self.request.user.role == "client" or (
            self.request.user.role == "" and not request.user.is_superuser
        ):
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
        if self.request.user.role == "client" or (
            self.request.user.role == "" and not request.user.is_superuser
        ):
            queryset = queryset.filter(user=request.user)

        serializer = UserCarSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        retrieved_car = get_object_or_404(UserCar, id=pk)
        print(retrieved_car)
        print(self.request.user.role)
        if (
            self.request.user.role == "client" and retrieved_car.user != request.user
        ) or (self.request.user.role == "" and not request.user.is_superuser):
            raise NotUser()
        serializer = UserCarSerializer(retrieved_car)
        return Response(serializer.data)

    def create(self, request):
        request_user = request.user
        data_brand = request.data["car_brand"]
        data_model = request.data["car_model"]
        model_brand = CarModel.objects.filter(id=data_model, car_brand_id=data_brand)
        if model_brand.count() == 0:
            raise NoPairBrandModel()

        request_copy = request.data.copy()
        if request_user.role == "admin":
            car_user = request_copy["user"]
            user = CustomUser.objects.filter(id=car_user)
            if (
                (user.first().role == "admin" or user.first().is_superuser)
                and user.first().id != request_user.id
            ) or user.count() == 0:
                raise CannotCreateOrEditCarForSuperUserOrAnotherAdmin()

        if request_user.role == "client":
            car_user = request_copy["user"]
            print(car_user)
            user = CustomUser.objects.filter(id=car_user)
            if (
                user.first().role != "client"
                or (
                    user.first().role == "client" and user.first().id != request_user.id
                )
                or user.count() == 0
            ):
                raise CannotCreateCarForAnotherUser()

        serializer = UserCarSerializer(data=request_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        request_user = request.user
        retrieved_car = get_object_or_404(UserCar, id=pk)
        car_user = retrieved_car.user.id
        user = CustomUser.objects.filter(id=car_user)
        if request_user.role == "admin":
            if (
                user.first().is_superuser
                or (user.first().role == "admin" and user.first().id != request_user.id)
                or user.count() == 0
            ):
                raise CannotCreateOrEditCarForSuperUserOrAnotherAdmin()

        self.check_object_permissions(request, retrieved_car)
        serializer = UserCarSerializer(retrieved_car, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        request_user = request.user
        retrieved_car = get_object_or_404(UserCar, id=pk)
        car_user = retrieved_car.user.id
        user = CustomUser.objects.filter(id=car_user)
        if request_user.role == "admin":
            if (
                user.first().is_superuser
                or (user.first().role == "admin" and user.first().id != request_user.id)
                or user.count() == 0
            ):
                raise CannotCreateOrEditCarForSuperUserOrAnotherAdmin()

        self.check_object_permissions(request, retrieved_car)
        self.perform_destroy(retrieved_car)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
