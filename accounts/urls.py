from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('user-address', views.UserAddressAPIView, basename="user-address")
router.register('specialization', views.SpecializationAPIView, basename='specialization')
router.register('journalist', views.JournalistAPIView, basename='journalist')
urlpatterns = [
    path('',include(router.urls)),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('email-verification/<uid>/<token>/', views.VerifyEmailView.as_view(), name='email-verification'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile/change-password/', views.PasswordChangeView.as_view(), name='change-password'),
    path('password-reset/', views.PasswordResetRequestAPIView.as_view(), name='password-reset'),
    path('password-reset/confirm/<uid>/<token>/', views.PasswordResetConfirmationAPIView.as_view(), name='password-reset'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='logout'),
]
