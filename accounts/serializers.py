from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = models.User
        fields = [
            "profile_image",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "date_of_birth",
            "bio",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            serializers.ValidationError("Password and confirm password don't match.")

        try:
            validate_password(password=password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop(
            "confirm_password"
        )  # remove confirm password before create an new user instance
        user = models.User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["profile_image", "username", "first_name", "last_name", "email", "date_of_birth", "bio"]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password  = serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate_old_password(self, value):
        user = self.context.get('request').user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    
    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        
        if new_password != confirm_password:
            serializers.ValidationError("New password and confirm password don't match.")

        try:
            validate_password(password=new_password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs
    
    def save(self):
        user = self.context.get('request').user
        user.set_password(self.validated_data.get('new_password')) # Hashing the password 
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if not models.User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        
        return value

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        
        if new_password != confirm_password:
            serializers.ValidationError("New password and confirm password don't match.")

        try:
            validate_password(password=new_password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAddress
        fields = ['user','country','city', 'zip_code']
        extra_kwargs = {
            "user": {"read_only": True},
        }

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialization
        fields = '__all__'
        
class JournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Journalist
        fields = '__all__'
        
        extra_kwargs = {
            "user": {"read_only": True},
        }

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = '__all__'
        
        extra_kwargs = {
            "subscriber": {"read_only": True},
        }
        