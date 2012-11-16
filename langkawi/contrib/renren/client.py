from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from langkawi.clients.oauth import OAuth2
from langkawi.settings import SESSION_KEY
from datetime import datetime
import json
import hashlib


class Renren(OAuth2):
    client_id = getattr(settings, 'RENREN_CLIENT_ID', '')
    secret = getattr(settings, 'RENREN_CLIENT_SECRET', '')
    scope = getattr(settings, 'RENREN_REQUEST_PERMISSIONS', 'publish_feed photo_upload')
    site = 'https://graph.renren.com/' #'https://login.renren.com/mlogin/'
    auth_url = 'oauth/authorize' #'auth/auth'
    access_token_url = 'oauth/token' #'auth/token'
    api_url = 'http://api.renren.com/restserver.do' #'http://api.m.renren.com/api/'
    expires = 30 * 24 * 3600
    _uid = None
    _user_info = None

    def get_callback_url(self):
        if self.is_https():
            return '%s%s' % (Site.objects.get_current().domain,
                reverse('langkawi:renren:callback'))
        return '%s%s' % (Site.objects.get_current().domain,
            reverse('langkawi:renren:callback'))

    def get_access_token(self, **params):
        params['grant_type'] = 'authorization_code'
        return super(Renren, self).get_access_token(**params)

    def parse_access_token(self, content):
        return json.loads(content)

    def api_reqeust(self, method):
        call_id = datetime.now().microsecond
        v = '1.0'
        access_token = self.get_access_token()
        sig_string = 'access_token=' + access_token + 'format=JSON' + 'method=' + method + 'v=' + v
        sig_string = sig_string + self.secret
        print sig_string
        sig = hashlib.md5(sig_string).hexdigest()
        params = {'method': method, 'sig': sig, 'v': v, 'format':'JSON'}
        #content = self.request('http://api.m.renren.com/api/profile/getInfo', 'POST', params)
        return self.request(self.api_url, 'POST', params)

    def get_user_info(self):
        if self._uid is None:
            #stupid Renren, get session key first
            response = self.api_reqeust('users.getInfo').json[0]
            print response
            self._uid = {'uid': response['uid']}
            self._user_info = {'name': response['name'], 'profile_image_url': response['headurl']}
            self._user_info.update(self._uid)
        return self._uid, self._user_info

    def create_friendships(self, user, profile):
        pass

    def send(self, status, filename=None):
        data = {'content': status}
        if filename is None:
            return self.r_post('statuses/update.json', data=data)
        pic = {'pic': open(filename, 'rb')}
        return self.r_upload('statuses/upload.json', pic, data=data)

    @staticmethod
    def get_session_key():
        return '%srenren' % SESSION_KEY
