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
    
@admin.register(models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['id', 'name', 'slug']
    ordering = ['created_at']
    
@admin.register(models.Journalist)
class JournalistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_specializations','languages', 'awards']
    list_filter = ['specialization','languages', 'awards']
    search_fields =['id', 'user', 'specialization','languages', 'awards']
    
    def get_specializations(self, obj):
        return obj.specialization.all()[0]
    
@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'subscriber', 'subscribed_to']
    search_fields =['id', 'subscriber', 'subscribed_to']


