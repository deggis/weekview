from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
#from deggis.weekgraph import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^deggis/', include('deggis.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^list/$', 'deggis.weekgraph.views.index'),
    (r'^image/$', 'deggis.weekgraph.views.image'),
    (r'^view/$', 'deggis.weekgraph.views.view'),
    (r'^admin/(.*)', admin.site.root)
)
