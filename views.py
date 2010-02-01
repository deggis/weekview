from django.http import HttpResponse
from django.template import Context, loader
from models import *
import django
from datetime import date
import imaging
from django.contrib.auth.decorators import login_required

"""Views for Weekview django application. Provides UI's and images from
HTTP requests."""

def solve_base():
	return django.root + '/weekview' # XXX: Get app name from smwhere else.

def index(request):
	"""Displays "home page" of the application."""

	t = loader.get_template('views/index.html')
	c = Context({
                'base': solve_base(),
		'user': 'deggis',
	})
	return HttpResponse(t.render(c))
index = login_required(index)

def image(request):
	"""Returns PNG image as HTTP response. Uses default values in none
	provided."""

	week, year = get_week_from_request(request)
	width, height = get_dimensions_from_request(request)
	image = imaging.draw_image(request.user, week, year, width, height)

	response = HttpResponse(mimetype="image/png")
	image.save(response, 'PNG')
	return response
image = login_required(image)


def get_week_from_request(request):
	if request.GET.__contains__("week") & request.GET.__contains__("year"):
		return int(request.GET["week"]), int(request.GET["year"])
	else:
                week = int(date.today().strftime("%W"))
                year = int(date.today().strftime("%Y"))
		return week, year

def get_dimensions_from_request(request):
	try:
		return (int(request.GET["x"]), int(request.GET["y"]))
	except:
		return (def_width, def_height)

def week(request):
	week, year = get_week_from_request(request)
	t = loader.get_template('views/week.html')
	c = Context({
                'base': solve_base(),
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

def show_buttons(request):
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
                'base': solve_base(),
		'user': 'deggis',
		'buttons': buttons,
		'clear_disabled': active_cat == None,
	})
	return HttpResponse(t.render(c))
show_buttons = login_required(show_buttons)

# FIXME: remove that if shit.
def register_button(request):
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

register_button = login_required(register_button)
