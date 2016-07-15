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

	def get(self, request):
		return Response({'mensaje' : 'Prueba envio de correo con mailgun GET'})

	def post(self, request):
	 	from_name = request.data["nameFrom"]
	 	to_name = request.data["nameTo"]
	 	contactName = request.data["contactName"]
	 	contactEmail = request.data["contactEmail"]
	 	contactMessage = request.data["contactMessage"]
	 	
	 	mail = MailLog()
		mail.from_field = 'postmaster@chailate.com'
		mail.to_field = request.data["mailTo"]
		mail.subject_field = request.data["subject"]

	 	body_mail = '''<h1>Super titulo de mail</h1><p>
	 	Contacto: {0} <br/>Nombre: {1} <br/>
	 	Mensaje: {2}</p><br/><b>
	 	Chailate rules!!</b>'''.format(
	 		contactEmail,contactName, contactMessage)
	 	
		mail.body_field = body_mail

	 	result = self.sendMail_usingMailgun(mail, from_name, to_name)

		return Response(result)

	def save_maillog(self, maildata):
		maildata.save()

	def sendMail_usingMailgun(self, mail, from_name, to_name):

		#Default response
		result = { 'result_code' : '0', 'error' : '' }		

		##Get mailgun api from environment
	 	mailgun_api = os.environ.get("MAILGUN_API", None)
	 	##If mailgun api is not definef return a error
	 	if mailgun_api is None:
	 		result['result_code'] = '500'
			result['error'] = 'Mailgun api is not set'
	 		return Response(result)

	 	try:
	 		mail.full_clean()
	 		print 'No errors'
	 	except ValidationError as ex:
	 		print 'Error'
	 		print str(ex)
	 		# non_field_errors = ex.message_dict[NON_FIELD_ERRORS]
	 		# print non_field_errors

		try:
			mail_response = requests.post(
	        "https://api.mailgun.net/v3/chailate.com/messages",
	        auth=("api", mailgun_api),
	        data={"from": "{0} <{1}>".format(from_name, mail.from_field),
	              "to": "{0} <{1}>".format(to_name, mail.to_field),
	              "subject": mail.subject_field,
	              "html": mail.body_field})

			##Save mail log in DB
			# self.save_maillog(mail)

			result['result_code'] = mail_response.status_code
		except Exception,e:
			result['result_code'] = '500'
			result['error'] = str(e)
			print str(e)

		return result
