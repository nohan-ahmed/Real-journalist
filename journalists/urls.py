from rest_framework.routers import DefaultRouter

from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('specialization', views.SpecializationAPIView, basename='specialization')
router.register('', views.JournalistAPIView, basename='journalist')

urlpatterns = [
    path('',include(router.urls)),
    path('subscribe/', views.SubscriptionAPIView.as_view(), name='subscribe'),
]
