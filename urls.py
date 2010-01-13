from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^image/$', 'weekview.views.image'),
    (r'^week/$', 'weekview.views.week'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'views/login.html'}),
    (r'^$', 'weekview.views.index'),
)
