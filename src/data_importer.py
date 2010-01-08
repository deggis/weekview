#!/usr/bin/env python
import os
import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from weekgraph.models import State, Transition

file = open("dataa.txt")
for line in file.readlines():
	print line.replace("\n", '')
	print " -> "
	tiedot = line.split(' ')
	vuosi,kuukausi,paiva = tiedot[0].split('-')
	tunnit,minuutit = tiedot[1].split(':')
        paivays	= datetime.datetime(int(vuosi),int(kuukausi),int(paiva),int(tunnit),int(minuutit),0)
	tila = State.objects.get(description=tiedot[2].replace("\n", ''))
	siirtyma = Transition(state=tila, timestamp=paivays)
	print siirtyma.__str__() + "\n"
	siirtyma.save()
