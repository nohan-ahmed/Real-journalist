from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": (
            "first_name",
            "last_name", 
            "email", 
            "password", 
            "date_of_birth")}
        ),
        ("Permissions", {"fields": (
            "is_staff", 
            "is_active", 
            "groups", 
            "user_permissions")}
        ),
    )
    add_fieldsets = (
        ( None, {"fields": (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "date_of_birth",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)