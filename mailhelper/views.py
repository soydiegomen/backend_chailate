from django.shortcuts import render
from django.contrib.auth.models import User
from serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.parsers import JSONParser
##Send mails using mailgun (Must install requests for python)
import requests
##Read environment variables
import os
from .models import (
	MailLog
	)

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
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = UserSerializer
	queryset = User.objects.all()

###Send Email
class SendMail(APIView):
	parser_classes = (JSONParser,)

	def save_maillog(self, maildata):
		maildata.save()

	def get(self, request):
		

		return Response({'mensaje' : 'Prueba envio de correo con mailgun GET'})
	def post(self, request):
	 	#from_mail = "Agencia Chailate"
	 	# to_mail = "dimegan@gmail.com"
	 	from_mail = request.data["nameFrom"]
	 	to_mail = request.data["mailTo"]
	 	to_name = request.data["nameTo"]
	 	
	 	contactName = request.data["contactName"]
	 	contactEmail = request.data["contactEmail"]
	 	contactMessage = request.data["contactMessage"]
	 	subject_mail = request.data["subject"]

	 	body_mail = ("<h1>Super titulo de mail</h1><p>Contacto: " 
	 		+ contactEmail +
	 		"<br/>Nombre:" 
	 		+ contactName +
	 		"<br/>Mensaje:" 
	 		+ contactMessage +
	 		"</p><br/>"
	 		"<b>Chailate rules!!</b>"
	 		)

	 	mail = MailLog()
		mail.from_field = 'dmendoza@mail.com'
		mail.to_field = to_mail
		mail.subject_field = subject_mail
		mail.body_field = body_mail

	 	result_status = "undefined"

	 	##Get mailgun api from environment
	 	mailgun_api = os.environ.get("MAILGUN_API", None)
	 	print mailgun_api

	 	##If mailgun api is not definef return a error
	 	if mailgun_api is None:
	 		return Response({'result' : result_status, 'error' : 'Mailgun api is not set' })
		
		try:
			result = requests.post(
	        "https://api.mailgun.net/v3/chailate.com/messages",
	        auth=("api", mailgun_api),
	        data={"from": from_mail + " <postmaster@chailate.com>",
	              "to": to_name+" <"+ to_mail +">",
	              "subject": subject_mail,
	              "html": body_mail})
			result_status = result.status_code
			##Save mail log in DB
			self.save_maillog(mail)
			print result.text
		except Exception,e:
			result_status = "Faild to send mail(exception)"
			print "faild to send mail"
			print str(e)

		return Response({'result' : result_status })

	