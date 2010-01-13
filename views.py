from django.http import HttpResponse
from django.template import Context, loader
from models import Transition, State
import datetime
from datetime import time
import webcolors
from django.contrib.auth.decorators import login_required

def getweek(begintime, endtime):
	return Transition.objects.filter(timestamp__gte=begintime,timestamp__lte=endtime).order_by('timestamp')

def getdays():
	return (begintime, endtime)


def drawtext(draw, text_pos, text):
	red = (180,180,180)
	draw.text(text_pos, text, fill=red)


def assign_to_day(transition, begindate):
#	slots = {26:0, 27:1, 28:2, 29:3, 30:4, 31:5, 1:6}
#	print begindate
#	print slots[begindate.day]
#	return slots[begindate.day]
	return begindate.weekday()

weekdays = ['MA','TI','KE','TO','PE','LA','SU']
secs_in_day = 24*60*60
padding_top = 50
def_height = 700
def_width = 1100

def evaluate_height(available_height, t):
	secs_in_event = (60*60*t.hour) + (60*t.minute) + (t.second)
	return available_height * (secs_in_event*1.0/secs_in_day)

def drawtransition(draw, height, width, transition, begintime):
	blue = (0,0,255)
	day = assign_to_day(transition, transition.timestamp.date())
	slot_width = width/7
	top = padding_top + evaluate_height((height-padding_top), transition.timestamp.time())
	bottom = height
	left = day*slot_width
	right = left+slot_width
	box = [left,top,right,bottom]
	draw.rectangle(box, fill=webcolors.hex_to_rgb('#'+transition.state.color))

	# Prepare for overnight happening
	draw.rectangle([left+slot_width, padding_top, right+slot_width, height], fill=webcolors.hex_to_rgb('#'+transition.state.color))
	text = transition.state.description + ' ' + transition.timestamp.time().strftime('%H:%M')
	drawtext(draw, (left+10,top+3), text)
	print "Tulostettiin transitio: %s" % transition
	print "\tlaatikkoon %s" % box

def getWeekFromRequest(request):
	if request.GET.__contains__("week"):
		return int(request.GET["week"])
	else:
		return 45

def getDimensionsFromRequest(request):
	try:
		return (int(request.GET["x"]), int(request.GET["y"]))
	except:
		return (def_width, def_height)


def drawGuideLines(draw, height, width):
	red = (255,0,0)
	blue = (0,0,255)
	toihin = (time(8,0,0, tzinfo=None), red)
	toista = (time(16,0,0, tzinfo=None), red)
	nukkumaan = (time(22,30, tzinfo=None), blue)
	heratys = (time(6,50,tzinfo=None), blue)
	viivat = [heratys,toihin,toista,nukkumaan]
	for viiva in viivat:
		korkeus = evaluate_height(height-padding_top, viiva[0])+padding_top
		draw.line((0, korkeus, width, korkeus), fill=viiva[1])

def image(request):
	week = getWeekFromRequest(request)
	width, height = getDimensionsFromRequest(request)
	print "Aloitetaan kuva"
	import Image, ImageDraw 
	size = (width,height)
	im = Image.new('RGB', size)
	draw = ImageDraw.Draw(im)

	begintime = datetime.date(2009, 1, 1)
	begintime = begintime + datetime.timedelta(days=-begintime.weekday(), weeks=week)
	endtime = begintime + datetime.timedelta(weeks=1)
	for i in range(7):
		day = begintime + datetime.timedelta(days=i)
		drawtext(draw, (10+(width/7*i), 10), "%s %s.%s." % (weekdays[i], day.day, day.month))

	transitions = getweek(begintime, endtime)
	for transition in transitions:
		drawtransition(draw, height, width, transition, begintime)

	drawGuideLines(draw, height, width)

	response = HttpResponse(mimetype="image/png")
	del draw
	im.save(response, 'PNG')
	print "Kuva piirretty responseen, valmis"
	return response
image = login_required(image)

def index(request):
	t = loader.get_template('views/index.html')
	c = Context({
		'user': 'deggis',
	})
	return HttpResponse(t.render(c))
index = login_required(index)

def week(request):
	week = getWeekFromRequest(request)
	t = loader.get_template('views/week.html')
	c = Context({
		'week': week,
		'prevweek': (week-1),
		'nextweek': (week+1),
	})
	return HttpResponse(t.render(c))
week = login_required(week)
