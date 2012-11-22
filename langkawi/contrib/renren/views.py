from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import View
from langkawi.contrib.renren.client import Renren
from langkawi.contrib.renren.models import RenrenProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback


class RenrenRedirect(OAuthRedirect):
    client = Renren
    template_name = 'langkawi/renren/renren.html'


class RenrenCallback(OAuthCallback):
    client = Renren
    template_name = 'langkawi/renren/renren.html'

    def get_redirect(self):
        return reverse('langkawi:renren:setup')


class RenrenSetup(SetupCallback):
    client = Renren
    profile = RenrenProfile
    template_name = 'langkawi/renren/renren.html'

    def get_lookup_kwargs(self, request, client):
        self.uid, user_info = client.get_user_info()
        return user_info

class RenrenUnbind(View):

    def post(self, request):
        if request.POST['unbind'] == '1' and request.user:
            try:
                renren_profile = RenrenProfile.objects.get(user=request.user)
                renren_profile.delete()
                return HttpResponse(simplejson.dumps({'msg':'ok'}))
            except RenrenProfile.DoesNotExist:
                return HttpResponse(simplejson.dumps({'msg':'failed'}))
        else:
            return HttpResponse(simplejson.dumps({'msg':'bad request'}))
