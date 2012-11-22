from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import View
from langkawi.contrib.douban.client import Douban
from langkawi.contrib.douban.models import DoubanProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback


class DoubanRedirect(OAuthRedirect):
    client = Douban
    template_name = 'langkawi/douban/douban.html'


class DoubanCallback(OAuthCallback):
    client = Douban
    template_name = 'langkawi/douban/douban.html'

    def get_redirect(self):
        return reverse('langkawi:douban:setup')


class DoubanSetup(SetupCallback):
    client = Douban
    profile = DoubanProfile
    template_name = 'langkawi/douban/douban.html'

    def get_lookup_kwargs(self, request, client):
        self.uid, user_info = client.get_user_info()
        return user_info

class DoubanUnbind(View):

    def post(self, request):
        if request.POST['unbind'] == '1' and request.user:
            try:
                douban_profile = DoubanProfile.objects.get(user=request.user)
                douban_profile.delete()
                return HttpResponse(simplejson.dumps({'msg':'ok'}))
            except DoubanProfile.DoesNotExist:
                return HttpResponse(simplejson.dumps({'msg':'failed'}))
        else:
            return HttpResponse(simplejson.dumps({'msg':'bad request'}))
