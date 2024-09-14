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
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
# Imports local modules
from . import models
from . import serializers
from .utils import get_tokens_for_user
from .permistions import IsOwnerOrReadOnly, UserAddressIsOwnerOrReadOnly, IsAdminOrReadOnly
# Create your views here.


class RegisterAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
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

class VerifyEmailView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
    def get(self, request, uid, token, format=None):
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            return Response({'error': 'Invalid verification link.'}, status=status.HTTP_404_NOT_FOUND)
        
        # validate the token
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)
   
class ProfileView(RetrieveUpdateDestroyAPIView):
    queryset= models.User.objects.all()
    serializer_class = serializers.UserSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsOwnerOrReadOnly]
    
class PasswordChangeView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'PasswordChangeAPI'
    permission_classes=[IsAuthenticated]
    
    def put(self, request, format=None):
        serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Message':'Passwrod changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetRequestAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
    
    def post(self, request, format=None):
        serializer= serializers.PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = models.User.objects.get(email=serializer.validated_data.get('email'))
            
            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create the password reset link
            reset_link = f"{request.build_absolute_uri('/user/password-reset/confirm/')}{uid}/{token}/"
            
            # Send the email
            subject = "Password Reset Request"
            message = render_to_string('./accounts/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(subject, strip_tags(message), settings.DEFAULT_FROM_EMAIL, [user.email])
            
            return Response({'message': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmationAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
    
    def post(self, request, uid, token, format=None):
        user_id = urlsafe_base64_decode(smart_str(uid))
        user = models.User.objects.get(pk=user_id)
        
        if user is not None and default_token_generator.check_token(user, token):
            serializer = serializers.PasswordResetSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.validated_data.get('new_password')) # Hash the password
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    scope = 'RegistrationAPI'
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":'User logout successfully!'},status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserAddressAPIView(ModelViewSet):
    queryset = models.UserAddress.objects.all()
    serializer_class = serializers.UserAddressSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [UserAddressIsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class SpecializationAPIView(ModelViewSet):
    queryset = models.Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes= [IsAdminOrReadOnly]