from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson
from django.views.generic import View
from langkawi.contrib.qq.client import QQ
from langkawi.contrib.qq.models import QQProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback, UnbindingView


class QQRedirect(OAuthRedirect):
    client = QQ
    template_name = 'langkawi/qq/qq.html'


class QQCallback(OAuthCallback):
    client = QQ
    template_name = 'langkawi/qq/qq.html'

    def get_redirect(self):
        return reverse('langkawi:qq:setup')


class QQSetup(SetupCallback):
    client = QQ
    profile = QQProfile
    template_name = 'langkawi/qq/qq.html'

    def get_lookup_kwargs(self, request, client):
        self.uid, user_info = client.get_user_info()
        return user_info

class QQUnbind(UnbindingView):
    profile = QQProfile
