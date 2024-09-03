from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.utils import timezone
from django.conf import settings

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Imports local modules
from . import models
from . import serializers

# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data.setdefault("is_active", False)
            user = serializer.save()
            
            # Send confirmation mail to user.
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"{request.build_absolute_uri('/user/email-verification/')}{uid}/{token}/"
            
            subject = "Confirm your email"
            message = render_to_string('./accounts/email_verification.html',{
                'request':user,
                'verification_link':verification_link
            })
            
            send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
