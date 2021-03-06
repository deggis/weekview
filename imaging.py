import webcolors
import datetime
import time
from events import *


"""Tools for drawing pictures. Uses Python Imaging Library."""

weekdays = ['MA','TI','KE','TO','PE','LA','SU']
secs_in_day = 24*60*60
padding_top = 50

def draw_image(user, week, year, width=800, height=600):
	"""Returns PNG image of week of the requested user."""

	import Image, ImageDraw 
	size = (width,height)
	im = Image.new('RGB', size)
	draw = ImageDraw.Draw(im)

        tday,tmonth = solve_first_day_of_week(week, year)
	begintime = datetime.date(year, tmonth, tday)
	endtime = begintime + datetime.timedelta(weeks=1)
	for i in range(7):
		day = begintime + datetime.timedelta(days=i)
		draw_text(draw, (5+(width/7*i), 10), "%s %s.%s." % (weekdays[i], day.day, day.month))

	events = get_events(begintime, endtime, user)
	for event in events:
		draw_event(draw, height, width, event, begintime)

	draw_guide_lines(draw, height, width)

	del draw
	return im

def evaluate_height(available_height, t):
	secs_in_event = (60*60*t.hour) + (60*t.minute) + (t.second)
	return available_height * (secs_in_event*1.0/secs_in_day)

def draw_guide_lines(draw, height, width):
	"""Because having image top as 00:00 and bottom as 23:59 isn't natural,
	some guide lines are useful."""

	red = (255,0,0)
	blue = (0,0,255)
	toihin = (datetime.time(8,0,0, tzinfo=None), red)
	toista = (datetime.time(16,0,0, tzinfo=None), red)
	nukkumaan = (datetime.time(22,30, tzinfo=None), blue)
	heratys = (datetime.time(6,50,tzinfo=None), blue)
	viivat = [heratys,toihin,toista,nukkumaan]
	for viiva in viivat:
		korkeus = evaluate_height(height-padding_top, viiva[0])+padding_top
		draw.line((0, korkeus, width, korkeus), fill=viiva[1])

def draw_text(draw, text_pos, text):
	color = (180,180,180)
	draw.text(text_pos, text, fill=color)

def draw_event(draw, height, width, event, begintime):
	box = solve_box_corners(event, height, width)
	draw.rectangle(box, fill=webcolors.hex_to_rgb('#'+event.category.color))

	text = event.begin.time().strftime('%H:%M') + ' ' + event.category.name
	if event.split_tail is False:
		draw_text(draw, (box[0],box[1]+3), text)

def solve_box_corners(event, height, width):
	slot_width = width/7
	top = padding_top + evaluate_height((height-padding_top), event.begin.time())
        bottom = padding_top + evaluate_height((height-padding_top), event.end.time())

	day = assign_to_day(event)
	left = day*slot_width
	right = left+slot_width

	return [left,top,right,bottom]
