from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db import models

# Create your models here.

class questions(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	question = models.CharField(max_length=180, unique=True)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	
	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = 'Question'
		verbose_name_plural = 'Questions'

	def __str__(self):
		return self.question

class answers(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
	question_ref = models.ForeignKey('questions', related_name='app_answer', on_delete=models.CASCADE)
	app_name = models.CharField(max_length=50)
	app_url = models.CharField(max_length=200)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	
	class Meta:
		ordering = ["-timestamp", "-updated"]
		verbose_name = 'Answer'
		verbose_name_plural = 'Answers'

	def __str__(self):
		return self.app_name