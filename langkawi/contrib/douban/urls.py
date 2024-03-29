from django.conf import settings
from django.conf.urls.defaults import *
from langkawi.contrib.douban.views import DoubanRedirect, \
    DoubanCallback, DoubanSetup, DoubanUnbind
urlpatterns = patterns('',
    url('^redirect/$', DoubanRedirect.as_view(), name='redirect'),
    url('^callback/$', DoubanCallback.as_view(), name='callback'),
    url('^setup/$', DoubanSetup.as_view(), name='setup'),
    url('^unbind/$',DoubanUnbind.as_view(), name='unbind')
)
