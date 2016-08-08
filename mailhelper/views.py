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
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.conf import settings

# Create your views here.

class HolaMundo(APIView):
	def get(self, request, nombre, format=None):
		print 'Mailgun api'
		if hasattr(settings, 'MAILGUN_API'):
			print settings.MAILGUN_API
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

	def get(self, request):
		return Response({'mensaje' : 'Prueba envio de correo con mailgun GET'})

	def post(self, request):
	 	from_name = request.data["nameFrom"]
	 	to_name = request.data["nameTo"]
	 	contactName = request.data["contactName"].encode('utf8')
	 	contactEmail = request.data["contactEmail"].encode('utf8')
	 	contactMessage = request.data["contactMessage"].encode('utf8')
	 	
	 	mail = MailLog()
	 	##User default for send mails
		mail.from_field = 'postmaster@chailate.com' 
		mail.to_field = request.data["mailTo"]
		mail.subject_field = request.data["subject"]

	 	mail.body_field = '''<h1>Super titulo de mail</h1><p>
	 	Contacto: {0} <br/>Nombre: {1} <br/>
	 	Mensaje: {2}</p><br/><b>
	 	Chailate rules!!</b>'''.format(
	 		contactEmail,contactName, contactMessage)

	 	result = self.sendMail_usingMailgun(mail, from_name, to_name)

		return Response(result)

	def sendMail_usingMailgun(self, mail, from_name, to_name):
		#Default response
		result = { 'result_code' : '0', 'error' : '' }		
		
	 	mailgun_api = ''
	 	##If mailgun api is not definef return a error
	 	if hasattr(settings, 'MAILGUN_API'):
	 		##Get mailgun api from settings file
			mailgun_api = settings.MAILGUN_API
		else:
	 		result['result_code'] = '500'
			result['error'] = 'Mailgun api is not set'
	 		return result
 	
		try:
			##Validate data before send mail and save log
	 		mail.full_clean()

	 		##Sen Mail using mailgun
			mail_response = requests.post(
	        "https://api.mailgun.net/v3/chailate.com/messages",
	        auth=("api", mailgun_api),
	        data={"from": "{0} <{1}>".format(from_name, mail.from_field),
	              "to": "{0} <{1}>".format(to_name, mail.to_field),
	              "subject": mail.subject_field,
	              "html": mail.body_field})

			result['result_code'] = mail_response.status_code

			##Save mail log in DB
			mail.save()
			
		except ValidationError as ex:
	 		error_message = ''
	 		##Loop dictionary with errors
	 		for k in ex.message_dict:
	 			error_message += error_message.join(ex.message_dict[k])

	 		result['result_code'] = '500'
	 		result['error'] = error_message
		except Exception,e:
			result['result_code'] = '500'
			result['error'] = str(e)

		return result
