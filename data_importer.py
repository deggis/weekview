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
			try:
				category = EventCategory.objects.get(name__iexact=name) # FIXME: add user check
				catdict[name.lower()] = category
			except Exception as inst:
				print "Category '"+name+"' was not found!"
				raise Exception('Error in data', 'DB does not contain category: '+name)
	return catdict

def parse_date(str):
	datestr, timestr = str.split(' ')
	year,month,day = datestr.split('.')
	hour,minute = timestr.split(':')
	try:
		return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),0)
	except Exception as inst:
		print "Invalid datestring: '"+str+"', got: "+inst.__str__()

def get_user(username):
	return User.objects.get(username__iexact=username)

def import_file(filename, username):
	catdict = get_categories(filename, username)
	user = get_user(username)
	file = open(filename)
	print """Beginning to import data. All needed categories were found!

"""
	for line in file.readlines():
		line = line.replace("\n", '')
		catstr, beginstr, endstr = line.split('|')

		event = Event()
		event.user = user
		event.category = catdict[catstr.lower()]
		event.begin = parse_date(beginstr)
		event.end = parse_date(endstr)
		print event.__str__()
		event.save()
	print """

There was many datas and the datas were good!

Byebye."""

import_file('data.txt', 'deggis')
