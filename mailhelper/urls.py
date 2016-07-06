from django.conf.urls import patterns,include, url
from rest_framework.urlpatterns import format_suffix_patterns
from views import (
	HolaMundo,
	AllUsers,
	GetUser
)

urlpatterns = patterns('mailhelper.views',
	url(r'^hola_mundo_rest/(?P<nombre>\w+)/$', HolaMundo.as_view()),
    url(r'^allusers/$', AllUsers.as_view()),    
    url(r'^getuser/(?P<pk>\d+)/$', GetUser.as_view()),    
)

urlpatterns = format_suffix_patterns(urlpatterns)