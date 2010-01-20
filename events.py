from models import *
import datetime
import time

"""Provides methods for accessing events in database, tools
for handling them and the calendar logic."""

class DrawableEvent:
	def __init__(self, user, category, begin, end):
		self.user = user
		self.category = category
		self.begin = begin
		self.end = end

# Get events + split overnight events to two events
def getEvents(begintime, endtime):
	events = []
	dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime).order_by('begin')
	for dbe in dbevents:
		event = DrawableEvent(dbe.user, dbe.category, dbe.begin, dbe.end)
		# FIXME: if overnight then split - here
		events.append(dbe)
	return events

def solveFirstDayOfWeek(week, year):
        t = time.strptime('%s %s 1' % (year, week), '%Y %W %w')
	return t.tm_mday, t.tm_mon

def assignToDay(event, begindate):
	return begindate.weekday()

