from django.shortcuts import render
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

# Create your views here.

class HolaMundo(APIView):
	def get(self, request, nombre, format=None):
		return Response({'mensaje' : 'Hola Mundo API rest', 'miname' : 'Mi nombre es->' + nombre})

class AllUsers(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

class GetUser(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()

class GetUsers(generics.ListCreateAPIView):
	permission_classes = [permissions.IsAuthenticated, TokenHasScope]
	serializer_class = UserSerializer
	queryset = User.objects.all()