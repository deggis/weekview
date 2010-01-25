#!/usr/bin/env python
import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from weekview.models import EventCategory, Event
from django.contrib.auth.models import User

def get_categories(filename, username):
	catdict = {}
	file = open(filename)
	for line in file.readlines():
		name = line.split('|')[0]
		if not name in catdict:
			category = EventCategory.objects.get(name__iexact=name) # FIXME: add user check
			if category is not None:
				catdict[name.lower()] = category
			else:
				raise Exception('Error in data', 'DB does not contain category: '+name)
	return catdict

def parse_date(str):
	datestr, timestr = str.split(' ')
	day,month,year = datestr.split('.')
	hour,minute = timestr.split(':')
	return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),0)

def get_user(username):
	return User.objects.get(username__iexact=username)

def import_file(filename, username):
	catdict = get_categories(filename, username)
	user = get_user(username)
	file = open(filename)
	for line in file.readlines():
		line = line.replace("\n", '')
		catstr, beginstr, endstr = line.split('|')

		event = Event()
		event.user = user
		event.category = catdict[catstr.lower()]
		event.begin = parse_date(beginstr)
		event.end = parse_date(endstr)
		print event.__str__() + "\n"
		event.save()

import_file('data.txt', 'deggis')
