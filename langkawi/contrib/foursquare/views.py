from django.core.urlresolvers import reverse
from langkawi.contrib.foursquare.client import Foursquare
from langkawi.contrib.foursquare.models import FoursquareProfile
from langkawi.views import OAuthRedirect, OAuthCallback, SetupCallback

class FoursquareRedirect(OAuthRedirect):
    client = Foursquare
    template_name = 'langkawi/foursquare/foursquare.html'

class FoursquareCallback(OAuthCallback):
    client = Foursquare
    template_name = 'langkawi/foursquare/foursquare.html'
    
    def get_redirect(self):
        return reverse('langkawi:foursquare:setup')

class FoursquareSetup(SetupCallback):
    client = Foursquare
    profile = FoursquareProfile
    template_name = 'langkawi/foursquare/foursquare.html'
    
    def get_lookup_kwargs(self, request, client):
        return {'foursquare': client.get_user_info()['id']}
    
