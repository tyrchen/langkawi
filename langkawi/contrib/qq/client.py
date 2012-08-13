from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
import json
from pprint import pprint


class QQ(OAuth2):
    client_id = getattr(settings, 'QQ_CLIENT_ID', '')
    secret = getattr(settings, 'QQ_CLIENT_SECRET', '')
    scope = getattr(settings, 'QQ_REQUEST_PERMISSIONS', '')
    site = 'https://graph.qq.com/'
    auth_url = 'oauth2.0/authorize'
    access_token_url = 'oauth2.0/token'
    expires = 30 * 24 * 3600

    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return 'https://%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:qq:callback'))
        return 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:qq:callback'))

    def get_access_token(self, **params):
        return super(QQ, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def get_user_info(self):
        if self._user_info is None:
            content = self.request('https://graph.qq.com/oauth2.0/me')
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
        return '%sqq' % SESSION_KEY
