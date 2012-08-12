from django.core.urlresolvers import reverse
from socialregistration.contrib.qq.client import QQ
from socialregistration.contrib.qq.models import QQProfile
from socialregistration.views import OAuthRedirect, OAuthCallback, SetupCallback


class QQRedirect(OAuthRedirect):
    client = QQ
    template_name = 'socialregistration/qq/qq.html'


class QQCallback(OAuthCallback):
    client = QQ
    template_name = 'socialregistration/qq/qq.html'

    def get_redirect(self):
        return reverse('socialregistration:qq:setup')


class QQSetup(SetupCallback):
    client = QQ
    profile = QQProfile
    template_name = 'socialregistration/qq/qq.html'

    def get_lookup_kwargs(self, request, client):
        return {'qq': client.get_user_info()}
