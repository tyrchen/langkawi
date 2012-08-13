from django.conf import settings
from django.conf.urls.defaults import *
from langkawi.contrib.weibo.views import WeiboRedirect, \
    WeiboCallback, WeiboSetup
urlpatterns = patterns('',
    url('^redirect/$', WeiboRedirect.as_view(), name='redirect'),
    url('^callback/$', WeiboCallback.as_view(), name='callback'),
    url('^setup/$', WeiboSetup.as_view(), name='setup'),
)
