from django.core.urlresolvers import reverse
from langkawi.contrib.douban.client import Douban
from langkawi.contrib.douban.models import DoubanProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback, UnbindingView


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

class DoubanUnbind(UnbindingView):
    profile = DoubanProfile