from models import *
import datetime
from datetime import timedelta
import time

"""Provides methods for accessing events in database, tools
for handling them and the calendar logic."""

def split_event(e):
    dayend = datetime.datetime(e.begin.year, e.begin.month, e.begin.day, 23, 59, 59)
    daybegin = datetime.datetime(e.end.year, e.end.month, e.end.day, 0, 0, 0)
    event1 = clone_event(e)
    event2 = clone_event(e)
    event1.end = dayend
    event2.begin = daybegin
    event2.split_tail = True
    return event1, event2

def clone_event(event):
    e = Event()
    e.user = event.user
    e.category = event.category
    e.description = event.description
    e.begin = event.begin
    e.end = event.end
    e.split_tail = False
    e.save = None # These event ARE not for saving
    return e

# Get events + split overnight events to two events
def get_events(begintime, endtime, req_user, req_category=None):
    events = []
    if req_category is not None:
        dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime,user=req_user,category=req_category).order_by('begin')
    else:
        dbevents = Event.objects.filter(begin__gte=begintime,begin__lte=endtime,user=req_user).order_by('begin')
    for dbe in dbevents:
        event = clone_event(dbe)
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


def temp_get_events(username, catname, begin, end):
    from django.contrib.auth.models import User
    the_user = None
    cat = None
    try:
        the_user = User.objects.get(username__iexact=username)
    except:
        raise ValueError("Username %s was not found!"%username)
    try:
        cat = EventCategory.objects.get(name__iexact=catname, user=the_user)
    except:
        raise ValueError("User %s has no category %s!" % (username,catname) )
    return get_events_for_weeks(the_user, begin, end, cat)

def temp_print_weekly_durations(username, catname, begin=(01,2010), end=(10,2010)):
    events_by_weeks = temp_get_events(username, catname, begin, end)
    durations_by_weeks = dict()
    for week in events_by_weeks.keys():
        print "\n\nWeek %s:" % week
        week_duration = timedelta(0)
        for event in events_by_weeks[week]:
            event_duration = event.end - event.begin
            print "Calculating -- %s -- event delta: %s" % (event.__unicode__(), str(event_duration))
            week_duration += event_duration
        durations_by_weeks[week] = week_duration

    print "\n\nDurations:"
    overall_duration = timedelta(0)
    for week in durations_by_weeks.keys():
        week_duration = durations_by_weeks[week]
        print "Week %s: \t%s" % (week, week_duration)
        overall_duration += week_duration

    print "\nOverall duration: %s" % overall_duration

def temp_print_csv_for_events(username, catname, begin=(01,2010), end=(10,2010)):
    events_by_weeks = temp_get_events(username, catname, begin, end)
    print "CSV begins:\n"
    for week in events_by_weeks.keys():
        for event in events_by_weeks[week]:
            event_duration = event.end - event.begin
            day = event.begin.strftime("%d.%m.%Y")
            begin_hhmm = event.begin.strftime("%H:%M")
            end_hhmm = event.end.strftime("%H:%M")
            line = "%s;%s;%s;%s" % (day,begin_hhmm,end_hhmm,event.description)
            print line
