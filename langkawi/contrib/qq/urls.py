from django.conf import settings
from django.conf.urls.defaults import *
from langkawi.contrib.qq.views import QQRedirect, \
    QQCallback, QQSetup, QQUnbind
urlpatterns = patterns('',
    url('^redirect/$', QQRedirect.as_view(), name='redirect'),
    url('^callback/$', QQCallback.as_view(), name='callback'),
    url('^setup/$', QQSetup.as_view(), name='setup'),
    url('^unbind/$',QQUnbind.as_view(), name='unbind')
)
