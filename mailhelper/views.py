from django.shortcuts import render
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class HolaMundo(APIView):
	def get(self, request, nombre, format=None):
		return Response({'mensaje' : 'Hola Mundo API rest', 'miname' : 'Mi nombre es->' + nombre})

class AllUsers(APIView):
	serializer_class = UserSerializer

	def get(self, request, format=None):
		#books = Book.objects.all()
		users = User.objects.all()
		response = self.serializer_class(users, many=True)
		return Response(response.data)