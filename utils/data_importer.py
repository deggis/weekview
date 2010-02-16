#!/usr/bin/env python
import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from weekview.models import EventCategory, Event
from django.contrib.auth.models import User

def get_categories(filename, username):
    """Reads categories from txt. If some category is missing,
    it's added.
    
    """

    catdict = {}
    file = open(filename)
    the_user = get_user(username)
    for line in file.readlines():
        name = line.split('|')[0]
        if not name in catdict:
            try:
                category = EventCategory.objects.get(name__iexact=name, user=the_user)
                catdict[name.lower()] = category
            except Exception as inst: # specify exception
                print "Category '%s' for user %s was missing, it will be added."\
                  % (name, username)
                cat = EventCategory()
                cat.user = the_user
                cat.name = name
                cat.color = "ffff00"
                cat.description = "[Generated]"
                cat.save()
                catdict[name.lower()] = cat
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
    print """Beginning to import data. All needed categories are present.

"""
    for line in file.readlines():
        line = line.replace("\n", '')
        catstr, beginstr, endstr, descstr = line.split('|')

        event = Event()
        event.user = user
        event.category = catdict[catstr.lower()]
        event.begin = parse_date(beginstr)
        event.end = parse_date(endstr)
        event.description = descstr
        print event.__str__()
        event.save()
    print """

There was many datas and the datas were good!

Byebye."""

import_file('data.txt', 'deggis')
