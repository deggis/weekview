from django.db import models

class State(models.Model):
	description = models.CharField(max_length=200)
	color = models.CharField(max_length=6)
	def __unicode__(self):
		return self.description

class Transition(models.Model):
	state = models.ForeignKey(State)
	timestamp = models.DateTimeField()
	
	def __unicode__(self):
		return self.timestamp.__str__() + " -> " + self.state.__str__()
