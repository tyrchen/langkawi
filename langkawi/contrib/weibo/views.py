from django.core.urlresolvers import reverse
from socialregistration.contrib.weibo.client import Weibo
from socialregistration.contrib.weibo.models import WeiboProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback


class WeiboRedirect(OAuthRedirect):
    client = Weibo
    template_name = 'socialregistration/weibo/weibo.html'


class WeiboCallback(OAuthCallback):
    client = Weibo
    template_name = 'socialregistration/weibo/weibo.html'

    def get_redirect(self):
        return reverse('socialregistration:weibo:setup')


class WeiboSetup(SetupCallback):
    client = Weibo
    profile = WeiboProfile
    template_name = 'socialregistration/weibo/weibo.html'

    def get_lookup_kwargs(self, request, client):
        return {'weibo': client.get_user_info()}
