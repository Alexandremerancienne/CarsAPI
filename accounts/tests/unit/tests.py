from django.test import TestCase
from accounts.models import CustomUser


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(username="alex")

    def test_user_content(self):
        custom_user = CustomUser.objects.get(id=1)
        expected_user_name = "alex"
        self.assertEquals(custom_user.username, expected_user_name)
