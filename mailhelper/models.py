from django.db import models

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question

class MailLog(models.Model):
	from_field = models.EmailField()
	to_field = models.EmailField()
	subject_field = models.CharField(max_length=200)
	body_field = models.TextField()
	send_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	def __unicode__(self):
		return str(self.send_date)
	