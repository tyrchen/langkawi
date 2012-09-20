from django.core.urlresolvers import reverse
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
