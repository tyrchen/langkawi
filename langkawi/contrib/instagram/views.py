from django.core.urlresolvers import reverse
from langkawi.contrib.instagram.client import Instagram
from langkawi.contrib.instagram.models import InstagramProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback


class InstagramRedirect(OAuthRedirect):
    client = Instagram
    template_name = 'langkawi/instagram/instagram.html'


class InstagramCallback(OAuthCallback):
    client = Instagram
    template_name = 'langkawi/instagram/instagram.html'

    def get_redirect(self):
        return reverse('langkawi:instagram:setup')


class InstagramSetup(SetupCallback):
    client = Instagram
    profile = InstagramProfile
    template_name = 'langkawi/instagram/instagram.html'

    def get_lookup_kwargs(self, request, client):
        return {'instagram': client.get_user_info()}
