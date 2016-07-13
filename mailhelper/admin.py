from mailhelper.models import (
	Poll,
	MailLog
	)
from django.contrib import admin

# Register your models here.
admin.site.register(Poll)
admin.site.register(MailLog)