from django.core.urlresolvers import reverse
from langkawi.contrib.tumblr.client import Tumblr
from langkawi.contrib.tumblr.models import TumblrProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class TumblrRedirect(OAuthRedirect):
    client = Tumblr
    template_name = 'langkawi/tumblr/tumblr.html'

class TumblrCallback(OAuthCallback):
    client = Tumblr
    template_name = 'langkawi/tumblr/tumblr.html'
    
    def get_redirect(self):
        return reverse('langkawi:tumblr:setup')

class TumblrSetup(SetupCallback):
    client = Tumblr
    profile = TumblrProfile
    template_name = 'langkawi/tumblr/tumblr.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'tumblr': client.get_user_info()['name']}
    
