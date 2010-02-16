from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    color = models.CharField(max_length=6)

    def __unicode__(self):
        return "%s's %s" % (self.user.__str__(), self.name)

class Event(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(EventCategory)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s: %s, %s (%s - %s)" % \
          (self.user.__str__(), self.category.name, self.description, \
           self.begin.__str__(), self.end.__str__())

class EventUnfinished(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(EventCategory)
    begin = models.DateTimeField()

    def __unicode__(self):
        return "%s's %s (started at %s)" % \
          (self.user.__str__(), self.category.name, self.begin.__str__())
