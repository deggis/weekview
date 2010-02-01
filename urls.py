from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^image/$', 'weekview.views.image'),
    (r'^week/$', 'weekview.views.week'),
    (r'^buttons/register$', 'weekview.views.register_button'),
    (r'^buttons/$', 'weekview.views.show_buttons'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'views/login.html'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/deggis/projects/mysite/weekview/media/'}),
    (r'^$', 'weekview.views.index'),
)
