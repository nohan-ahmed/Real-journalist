from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "date_of_birth",
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = ("id", "username", "email", "first_name", "last_name")
    ordering = ("email","date_of_birth","date_joined")


@admin.register(models.UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'country','city', 'zip_code']
    list_filter = ['country','city', 'zip_code']
    search_fields = ['id', 'user', 'country','city', 'zip_code']
    ordering = ['country','city', 'zip_code']
    

