from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = models.User
        fields = ['profile_image','username', 'first_name', 'last_name', 'email','password','confirm_password', 'date_of_birth', 'bio']
        extra_kwargs = {'password':{'write_only':True}}
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            serializers.ValidationError("Password and confirm password don't match.")
            
        try:
            validate_password(password=password, user=None)
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password') # remove confirm password before create an new user instance
        user = models.User.objects.create_user(**validated_data)
        return user
    
    