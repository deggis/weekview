from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	description = models.CharField(max_length=200)
	color = models.CharField(max_length=6)
	def __unicode__(self):
		return self.description

class Event(models.Model):
        user = models.ForeignKey(User)
	category = models.ForeignKey(Category)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	def __unicode__(self):
		return self.timestamp.__str__() + " -> " + self.state.__str__()
