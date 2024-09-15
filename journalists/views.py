from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404

# DRF
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

# Imports local modules
from . import models
from . import serializers
from accounts.permistions import ObjectIsOwnerOrReadOnly, IsAdminOrReadOnly
# Create your views here.

# Create your views here.
class SpecializationAPIView(ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes= [IsAdminOrReadOnly]

class JournalistAPIView(ModelViewSet):
    queryset = models.Journalist.objects.all()
    serializer_class = serializers.JournalistSerializer
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
    permission_classes = [ObjectIsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        user = self.request.user

        # Check if a Journalist instance already exists for this user
        if models.Journalist.objects.filter(user=user).exists():
            raise ValidationError({"detail": "Journalist profile already exists for this user."})

        # If it doesn't exist, create a new instance
        serializer.save(user=user)
        subject = "Welcome to Real-Journalist – Your Journalist Account is Now Live!"
        message = render_to_string('./accounts/Journalist_account_create_email.html',{
                'user':user,
            })
            
        send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
        
class SubscriptionAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'SubscriptionAPI'
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = serializers.SubscriptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            subscriber=request.user
            subscribed_to = serializer.validated_data.get('subscribed_to')
            
            subscribe = models.Subscription.objects.filter(subscriber=subscriber, subscribed_to=subscribed_to).first()
            
            if subscribe is not None:
                subscribe.delete()
                return Response({'message':f'{subscriber} unsubscribed to {subscribed_to}'}, status=status.HTTP_204_NO_CONTENT)
            
            serializer.save(subscriber=subscriber) # if subscriber didn't follow this account it will create new instance for Subscription model
            return Response({'message':f'{subscriber} subscribed to {subscribed_to}'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
