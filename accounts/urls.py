from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
