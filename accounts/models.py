from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE = (
        ("admin", "Admin"),
        ("client", "Client"),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        blank=True,
        help_text="Role (Admin, Client)",
    )
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(blank=True, null=True)
