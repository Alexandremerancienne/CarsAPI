from django.test import TestCase
from api.models import CarBrand, CarModel, UserCar
from accounts.models import CustomUser


class CarBrandModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CarBrand.objects.create(name="Lada")

    def test_name_content(self):
        car_brand = CarBrand.objects.get(id=1)
        expected_brand_name = "Lada"
        self.assertEquals(car_brand.name, expected_brand_name)


class CarModelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_brand = CarBrand.objects.create(name="Lada")
        test_brand.save()

        CarModel.objects.create(car_brand=test_brand, name="Supreme")

    def test_name_content(self):
        car_model = CarModel.objects.get(id=1)
        expected_model_name = "Supreme"
        self.assertEquals(car_model.name, expected_model_name)


class UserCarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_brand = CarBrand.objects.create(name="Lada")
        test_brand.save()

        test_model = CarModel.objects.create(car_brand=test_brand, name="Supreme")
        test_model.save()

        test_user = CustomUser.objects.create(username="alex")
        test_user.save()

        UserCar.objects.create(
            user=test_user, car_brand=test_brand, car_model=test_model
        )

    def test_brand_content(self):
        user_car = UserCar.objects.get(id=1)
        expected_brand_name = "Lada"
        self.assertEquals(user_car.car_brand.name, expected_brand_name)

    def test_model_content(self):
        user_car = UserCar.objects.get(id=1)
        expected_model_name = "Supreme"
        self.assertEquals(user_car.car_model.name, expected_model_name)

    def test_user_content(self):
        user_car = UserCar.objects.get(id=1)
        expected_user_name = "alex"
        self.assertEquals(user_car.user.username, expected_user_name)
