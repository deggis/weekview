from django.http import HttpResponse
from django.template import Context, loader
from models import *
import datetime
import time
from datetime import date
import webcolors
from django.contrib.auth.decorators import login_required

def getEvents(begintime, endtime):
	return Event.objects.filter(begin__gte=begintime,end__lte=endtime).order_by('begin')

def getdays():
	return (begintime, endtime)

def drawtext(draw, text_pos, text):
	red = (180,180,180)
	draw.text(text_pos, text, fill=red)

def assignToDay(event, begindate):
	return begindate.weekday()

weekdays = ['MA','TI','KE','TO','PE','LA','SU']
secs_in_day = 24*60*60
padding_top = 50
def_height = 700
def_width = 1100

def evaluateHeight(available_height, t):
	secs_in_event = (60*60*t.hour) + (60*t.minute) + (t.second)
	return available_height * (secs_in_event*1.0/secs_in_day)

def drawEvent(draw, height, width, event, begintime):
	blue = (0,0,255)
	day = assignToDay(event, event.begin.date())
	slot_width = width/7
	top = padding_top + evaluateHeight((height-padding_top), event.begin.time())
	#bottom = height
        bottom = padding_top + evaluateHeight((height-padding_top), event.end.time())
	left = day*slot_width
	right = left+slot_width
	box = [left,top,right,bottom]
	draw.rectangle(box, fill=webcolors.hex_to_rgb('#'+event.category.color))

	# Prepare for overnight happening
	# draw.rectangle([left+slot_width, padding_top, right+slot_width, height], fill=webcolors.hex_to_rgb('#'+event.category.color))
	text = event.category.description + ' ' + event.begin.time().strftime('%H:%M')
	drawtext(draw, (left+10,top+3), text)
	print "Tulostettiin transitio: %s" % event
	print "\tlaatikkoon %s" % box

def getWeekFromRequest(request):
	if request.GET.__contains__("week") & request.GET.__contains__("year"):
		return int(request.GET["week"]), int(request.GET["year"])
	else:
                week = int(date.today().strftime("%W"))
                year = int(date.today().strftime("%Y"))
		return week, year

def solveFirstDayOfWeek(week, year):
        t = time.strptime('%s %s 1' % (year, week), '%Y %W %w')
	return t.tm_mday, t.tm_mon

def getDimensionsFromRequest(request):
	try:
		return (int(request.GET["x"]), int(request.GET["y"]))
	except:
		return (def_width, def_height)


def drawGuideLines(draw, height, width):
	red = (255,0,0)
	blue = (0,0,255)
	toihin = (datetime.time(8,0,0, tzinfo=None), red)
	toista = (datetime.time(16,0,0, tzinfo=None), red)
	nukkumaan = (datetime.time(22,30, tzinfo=None), blue)
	heratys = (datetime.time(6,50,tzinfo=None), blue)
	viivat = [heratys,toihin,toista,nukkumaan]
	for viiva in viivat:
		korkeus = evaluateHeight(height-padding_top, viiva[0])+padding_top
		draw.line((0, korkeus, width, korkeus), fill=viiva[1])

def image(request):
	week, year = getWeekFromRequest(request)
	width, height = getDimensionsFromRequest(request)
	import Image, ImageDraw 
	size = (width,height)
	im = Image.new('RGB', size)
	draw = ImageDraw.Draw(im)

        tday,tmonth = solveFirstDayOfWeek(week, year)
	begintime = datetime.date(year, tmonth, tday)
	endtime = begintime + datetime.timedelta(weeks=1)
	for i in range(7):
		day = begintime + datetime.timedelta(days=i)
		drawtext(draw, (10+(width/7*i), 10), "%s %s.%s." % (weekdays[i], day.day, day.month))

	events = getEvents(begintime, endtime)
	for event in events:
		drawEvent(draw, height, width, event, begintime)

	drawGuideLines(draw, height, width)

	response = HttpResponse(mimetype="image/png")
	del draw
	im.save(response, 'PNG')
	return response
image = login_required(image)

def index(request):
	t = loader.get_template('views/index.html')
	c = Context({
                'base': solveBase(),
		'user': 'deggis',
	})
	return HttpResponse(t.render(c))
index = login_required(index)

def solveBase():
	return 'http://cameron:8080/weekview' # FIXME

def week(request):
	week, year = getWeekFromRequest(request)
	t = loader.get_template('views/week.html')
	c = Context({
                'base': solveBase(),
		'user': 'deggis',
		'week': week,
                'year': year,
		'prevWeek': (week-1),
		'nextWeek': (week+1),
	})
	return HttpResponse(t.render(c))
week = login_required(week)

class CategoryButton:
	def __init__(self, category, enabled):
		self.category = category
		self.disabled = not enabled

def showButtons(request):
	categories = EventCategory.objects.filter(user=request.user).order_by('name')
	unfinished = EventUnfinished.objects.filter(user=request.user)
	if len(unfinished) == 1:
		active_cat = unfinished[0].category
	else:
		active_cat = None

	buttons = []
	for cat in categories:
		if cat == active_cat:
			state = False
		else:
			state = True # :)
		buttons.append(CategoryButton(cat, state))
	t = loader.get_template('views/buttons.html')
	c = Context({
                'base': solveBase(),
		'user': 'deggis',
		'buttons': buttons,
		'clear_disabled': active_cat == None,
	})
	return HttpResponse(t.render(c))
showButtons = login_required(showButtons)

def registerButton(request):
	unfinisheds = EventUnfinished.objects.filter(user=request.user)
	if request.POST["button"] == "Clear":
		tmp = unfinisheds[0]
		e = Event()
		e.user = tmp.user
		e.category = tmp.category
		e.begin = tmp.begin
		e.end = datetime.datetime.now()+datetime.timedelta(hours=10)
		e.save()
		tmp.delete()
		return HttpResponse("rekistered: " + e.__str__())
	else:
		if len(unfinisheds) == 1:
			tmp = unfinisheds[0]
			e = Event()
			e.user = tmp.user
			e.category = tmp.category
			e.begin = tmp.begin
			e.end = datetime.datetime.now()+datetime.timedelta(hours=10)
			e.save()
			tmp.delete()
		new = EventUnfinished()
		new.user = request.user
		new.category = EventCategory.objects.filter(name=request.POST["button"])[0]
		new.begin = datetime.datetime.now()+datetime.timedelta(hours=10)
		new.save()
		return HttpResponse("registered: " + new.__str__())

registerButton = login_required(registerButton)
