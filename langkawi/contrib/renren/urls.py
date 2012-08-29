from django.conf import settings
from django.conf.urls.defaults import *
from langkawi.contrib.renren.views import RenrenRedirect, \
    RenrenCallback, RenrenSetup
urlpatterns = patterns('',
    url('^redirect/$', RenrenRedirect.as_view(), name='redirect'),
    url('^callback/$', RenrenCallback.as_view(), name='callback'),
    url('^setup/$', RenrenSetup.as_view(), name='setup'),
)
