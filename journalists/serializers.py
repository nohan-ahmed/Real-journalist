from rest_framework import serializers
from . import models

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

