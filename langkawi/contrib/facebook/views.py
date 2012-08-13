from django.core.urlresolvers import reverse
from langkawi.contrib.facebook.client import Facebook
from langkawi.contrib.facebook.models import FacebookProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class FacebookRedirect(OAuthRedirect):
    client = Facebook
    template_name = 'langkawi/facebook/facebook.html'

class FacebookCallback(OAuthCallback):
    client = Facebook
    template_name = 'langkawi/facebook/facebook.html'
    
    def get_redirect(self):
        return reverse('langkawi:facebook:setup')

class FacebookSetup(SetupCallback):
    client = Facebook
    profile = FacebookProfile
    template_name = 'langkawi/facebook/facebook.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'uid': client.get_user_info()['id']}
