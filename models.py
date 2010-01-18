from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
        user = models.ForeignKey(User)
	name = models.CharField(max_length=20)
        description = models.CharField(max_length=200)
	color = models.CharField(max_length=6)
	def __unicode__(self):
		return self.user.__str__() + "'s " + self.name

class Event(models.Model):
        user = models.ForeignKey(User)
	category = models.ForeignKey(EventCategory)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	def __unicode__(self):
		return self.user.__str__() + ": " + self.category.name + " (" + self.begin.__str__() + " - " + self.end.__str__() + ")"

class EventUnfinished(models.Model):
        user = models.ForeignKey(User)
        category = models.ForeignKey(EventCategory)
        begin = models.DateTimeField()
        def __unicode__(self):
		return self.user.__str__() + "'s " + self.category.name + " (started at " + self.begin.__str__() + ")"
