from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import
# Imports local modules
from . import models
from . import serializers
# Create your views here.

class RegisterAPIView(APIView):
    def post(self, request, format=None):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            