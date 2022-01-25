from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("location",)}),
        (None, {"fields": ("role",)}),
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "role",
    )


admin.site.register(CustomUser, CustomUserAdmin)
