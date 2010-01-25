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
		self.split_tail = False

def split_event(e):
	dayend = datetime.datetime(e.begin.year, e.begin.month, e.begin.day, 23, 59, 59)
	daybegin = datetime.datetime(e.end.year, e.end.month, e.end.day, 0, 0, 0)
	event1 = DrawableEvent(e.user, e.category, e.begin, dayend)
	event2 = DrawableEvent(e.user, e.category, daybegin, e.end)
	event2.split_tail = True
	return event1, event2

# Get events + split overnight events to two events
def getEvents(begintime, endtime):
	events = []
	dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime).order_by('begin')
	for dbe in dbevents:
		event = DrawableEvent(dbe.user, dbe.category, dbe.begin, dbe.end)
		if dbe.begin.day != dbe.end.day: # If overnight, then split
			event1, event2 = split_event(event)
			events.append(event1)
			events.append(event2)
		else:
			events.append(event)
	return events

def solveFirstDayOfWeek(week, year):
        t = time.strptime('%s %s 1' % (year, week), '%Y %W %w')
	return t.tm_mday, t.tm_mon

def assignToDay(event, begindate):
	return begindate.weekday()

