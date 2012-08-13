from django.core.urlresolvers import reverse
from langkawi.contrib.weibo.client import Weibo
from langkawi.contrib.weibo.models import WeiboProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback


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
        return {'weibo': client.get_user_info()}
