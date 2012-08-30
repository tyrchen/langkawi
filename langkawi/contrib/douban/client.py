from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
import json
from pprint import pprint


class Douban(OAuth2):
    client_id = getattr(settings, 'DOUBAN_CLIENT_ID', '')
    secret = getattr(settings, 'DOUBAN_CLIENT_SECRET', '')
    scope = getattr(settings, 'DOUBAN_REQUEST_PERMISSIONS', '')
    site = 'https://www.douban.com/service/'
    auth_url = 'auth2/auth'
    access_token_url = 'auth2/token'
    expires = 30 * 24 * 3600

    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:douban:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:douban:callback'))

    def get_access_token(self, **params):
        return super(Douban, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def get_user_info(self):
        if self._user_info is None:
            content = self.request('http://api.douban.com/people/@me')
            pprint(content)
            self._user_info = content
            pprint(self._user_info)
        return self._user_info

    def send(self, status, filename=None):
        data = {'content': status}
        if filename is None:
            return self.r_post('statuses/update.json', data=data)
        pic = {'pic': open(filename, 'rb')}
        return self.r_upload('statuses/upload.json', pic, data=data)

    @staticmethod
    def get_session_key():
        return '%sdouban' % SESSION_KEY
