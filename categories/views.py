from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from .models import Category
from .serializers import CategorySerializer
from .permistions import IsAdminOrReadOnly
# Create your views here.

class CategoryAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAdminOrReadOnly]