from django.conf import settings
from django.conf.urls.defaults import *
from views import Logout, Setup

urlpatterns = patterns('',)

if 'langkawi.contrib.facebook' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^facebook/', include('langkawi.contrib.facebook.urls',
            namespace='facebook')))

if 'langkawi.contrib.foursquare' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^foursquare/', include('langkawi.contrib.foursquare.urls',
            namespace='foursquare')))

if 'langkawi.contrib.instagram' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^instagram/', include('langkawi.contrib.instagram.urls',
            namespace='instagram')))

if 'langkawi.contrib.weibo' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^weibo/', include('langkawi.contrib.weibo.urls',
            namespace='weibo')))

if 'langkawi.contrib.qq' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^qq/', include('langkawi.contrib.qq.urls',
            namespace='qq')))

if 'langkawi.contrib.renren' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^renren/', include('langkawi.contrib.renren.urls',
            namespace='renren')))

if 'langkawi.contrib.douban' in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + patterns('',
        url(r'^douban/', include('langkawi.contrib.douban.urls',
            namespace='douban')))

urlpatterns = urlpatterns + patterns('',
    url(r'^setup/$', Setup.as_view(), name='setup'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
)
