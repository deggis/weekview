from models import *
import datetime
from datetime import timedelta
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
    def __unicode__(self):
        return "%s event (%s - %s)" % (self.category,self.begin,self.end)

    def __str__(self):
        return self.__unicode__()

def split_event(e):
    dayend = datetime.datetime(e.begin.year, e.begin.month, e.begin.day, 23, 59, 59)
    daybegin = datetime.datetime(e.end.year, e.end.month, e.end.day, 0, 0, 0)
    event1 = DrawableEvent(e.user, e.category, e.begin, dayend)
    event2 = DrawableEvent(e.user, e.category, daybegin, e.end)
    event2.split_tail = True
    return event1, event2

# Get events + split overnight events to two events
def get_events(begintime, endtime, req_user, req_category=None):
    events = []
    if req_category is not None:
        dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime,user=req_user,category=req_category).order_by('begin')
    else:
        dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime,user=req_user).order_by('begin')
    for dbe in dbevents:
        event = DrawableEvent(dbe.user, dbe.category, dbe.begin, dbe.end)
        if dbe.begin.day != dbe.end.day: # If overnight, then split
            event1, event2 = split_event(event)
            add_if_applicable(events,begintime,endtime,event1)
            add_if_applicable(events,begintime,endtime,event2) 
        else:
            add_if_applicable(events,begintime,endtime,event)
    return events

def add_if_applicable(events,begintime,endtime,event):
    #if event.begin.date >= begintime:
    #    if event.end < endtime.date:
    # FIXME: Implement date comparisons
    events.append(event)

def get_events_for_weeks(user, begin_data, end_data, category=None):
    begin_date = solve_first_date_of_week(begin_data[0], begin_data[1])
    end_date = solve_first_date_of_week(end_data[0], end_data[1])
    if begin_date > end_date:
        raise ValueError("Invalid dates! End before start.")

    events_by_weeks = dict()
    d = 0
    while True:
        begin = solve_first_date_of_week(begin_data[0], begin_data[1]) + \
            timedelta(days=(7*d))
        end = begin + timedelta(days=7) - timedelta(seconds=1)
        if begin > end_date:
           break
        events_by_weeks[begin_data[0]+d] = []
        if(begin_data[0]+d)==43:
            print "begin: %s, end: %s" % (begin, end)

        events = get_events(begin, end, user, category)
        for event in events:
            events_by_weeks[begin_data[0]+d].append(event)
        d += 1
    return events_by_weeks

def solve_first_day_of_week(week, year):
    t = time.strptime('%s %s 1' % (year, week), '%Y %W %w')
    return t.tm_mday, t.tm_mon

def solve_first_date_of_week(week, year):
    day, mon = solve_first_day_of_week(week, year)
    return datetime.datetime(year,mon,day,0,0,0)        

def assign_to_day(event):
	return event.begin.weekday()

def temp_print_durations():
    from django.contrib.auth.models import User

    deg = User.objects.all()
    koulu = EventCategory.objects.all()[2]

    begin = (43,2009)
    end = (49,2009)

    events_by_weeks = get_events_for_weeks(deg, begin, end, koulu)
    durations_by_weeks = dict()
    for week in events_by_weeks.keys():
        print "\n\nWeek %s:" % week
        week_duration = timedelta(0)
        for event in events_by_weeks[week]:
            event_duration = event.end - event.begin
            print "Adding %s event delta: %s" % (event, str(event_duration))
            week_duration += event_duration
        durations_by_weeks[week] = week_duration

    print "\n\nDurations:"
    overall_duration = timedelta(0)
    for week in durations_by_weeks.keys():
        week_duration = durations_by_weeks[week]
        print "Week %s: \t%s" % (week, week_duration)
        overall_duration += week_duration

    print "\nOverall duration: %s" % overall_duration


