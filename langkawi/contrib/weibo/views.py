from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import View
from langkawi.contrib.weibo.client import Weibo
from langkawi.contrib.weibo.models import WeiboProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback
from pprint import pprint


class WeiboRedirect(OAuthRedirect):
    client = Weibo
    template_name = 'langkawi/weibo/weibo.html'


class WeiboCallback(OAuthCallback):
    client = Weibo
    template_name = 'langkawi/weibo/weibo.html'

    def get_redirect(self):
        return reverse('langkawi:weibo:setup')


class WeiboSetup(SetupCallback):
    client = Weibo
    profile = WeiboProfile
    template_name = 'langkawi/weibo/weibo.html'

    def get_lookup_kwargs(self, request, client):
        self.uid, user_info = client.get_user_info()
        self.username = user_info['screen_name']
        return user_info

class WeiboUnbind(View):

    def post(self, request):
        if request.POST['unbind'] == '1' and request.user:
            try:
                Weibo_profile = WeiboProfile.objects.get(user=request.user)
                Weibo_profile.delete()
                return HttpResponse(simplejson.dumps({'msg':'ok'}))
            except WeiboProfile.DoesNotExist:
                return HttpResponse(simplejson.dumps({'msg':'failed'}))
        else:
            return HttpResponse(simplejson.dumps({'msg':'bad request'}))
