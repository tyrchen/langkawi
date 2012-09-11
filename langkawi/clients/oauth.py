from django.utils.translation import ugettext_lazy as _
from langkawi.clients import Client
import requests
import time
from requests_oauth2 import OAuth2 as oauth2
import urlparse
from pprint import pprint

class OAuthError(Exception):
    """
    Exception thrown when we run into OAuth{1,2} errors. This error is
    displayed to the end user in the default templates.
    """
    pass


class OAuth2(Client):
    """
    Base class for  services such as Facebook, Github and Foursquare.
    """

    # The client id provided by the service
    client_id = None

    # The secret id provided by the service
    secret = None

    # The hostname we'll be accessing
    site = None

    # The URL where we'll be requesting permissions from the user
    auth_url = None

    # The URL where we'll be obtaining an access token once permissions were
    # granted
    access_token_url = None

    # The permission's we'll be asking for
    scope = None

    # The access token we obtained
    _access_token = None

    # The dict holding all infos we got from the access token endpoint
    access_token_dict = None

    # The date when access token will expire
    token_expires_in = 0.0

    # The URL where we'll be requesting api
    api_url = None
    upload_api_url = None

    # Memoized user info fetched once an access token was obtained
    _user_info = None

    # Use requests lib to do http requests
    _request = requests

    def __init__(self, access_token=None):
        self._access_token = access_token

    def oauth2_handler(self):
        return oauth2(self.client_id, self.secret, self.site, self.get_callback_url(), self.auth_url, self.access_token_url)

    def get_redirect_url(self, state=''):
        """
        Assemble the URL to where we'll be redirecting the user to to request
        permissions.
        """
        authorization_url = self.oauth2_handler().authorize_url(self.scope, response_type='code')
        pprint(authorization_url)
        return authorization_url

    def parse_access_token(self, content):
        """
        Parse the access token response. The default OAuth response should be
        a query string - but some services return JSON instead.
        """
        return dict(urlparse.parse_qsl(content))

    def request_access_token(self, params):
        """
        Request the access token from `self.access_token_url`. The default
        behaviour is to use a `POST` request, but some services use `GET`
        requests. Individual clients can override this method to use the
        correct HTTP method.
        """
        return self.request(self.access_token_url, method="POST", params=params,
            is_signed=False)

    def _get_access_token(self, code, **params):
        """
        Fetch an access token with the provided `code`.
        """
        content = self.oauth2_handler().get_token(code, **params)
        if 'error' in content:
            raise OAuthError(_(
                u"Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, content['error']))

        return content

    def get_access_token(self, code=None, **params):
        """
        Return the memoized access token or go out and fetch one.
        """
        if self._access_token is None:
            if code is None:
                raise ValueError(_('Invalid code.'))

            self.access_token_dict = self._get_access_token(code, **params)
            try:
                self._access_token = self.access_token_dict['access_token']
                if isinstance(self._access_token, list):
                    self._access_token = self._access_token[0]
                if 'expires_in' in self.access_token_dict:
                    expires_in = self.access_token_dict['expires_in']
                    if isinstance(expires_in, list):
                        expires_in = expires_in[0]
                    self.token_expires_in = int(expires_in) + int(time.time())
            except KeyError, e:
                raise OAuthError("Credentials could not be validated, the provider returned no access token.")

        return self._access_token

    def complete(self, GET):
        """
        Complete the OAuth2 flow by fetching an access token with the provided
        code in the GET parameters.
        """
        if 'error' in GET:
            raise OAuthError(
                _("Received error while obtaining access token from %s: %s") % (
                    self.access_token_url, GET['error']))
        return self.get_access_token(code=GET.get('code'))

    def get_signing_params(self):
        """
        Return the paramters for signing a request. Some APIs don't
        obey the standard `access_token` parameter - they can override this
        method and return their used parameters.
        """
        return dict(access_token=self._access_token)

    def is_expires(self):
        return not self._access_token or time.time() > self.token_expires_in

    # Basic http request
    def request(self, url, method="GET", params=None, headers=None, is_signed=True):
        """
        Make a request against ``url``. By default, the request is signed with
        an access token, but can be turned off by passing ``is_signed=False``.
        """
        params = params or {}
        headers = headers or {}
        if self.is_expires():
            raise OAuthError("Access token is expired")
        if is_signed:
            params.update(self.get_signing_params())
        if method == 'GET':
            return self._request.request(method, url, params=params, headers=headers)
        return self._request.request(method, url, data=params, headers=headers)

    # Another way to do http requests
    def request_hook(self, args):
        if self.is_expires():
            raise OAuthError("Access token is expired")
        if args.get('params') is not None:
            args['params'].update(self.get_signing_params())
        if args.get('data') is not None:
            args['data'] = self.get_signing_params()
        return args

    def r_get(self, url, params=None, headers=None):
        hooks = dict(args=self.request_hook)
        return self._request.get(self.api_url + url, hooks=hooks, params=params, headers=headers)

    def r_post(self, url, params=None, headers=None):
        hooks = dict(args=self.request_hook)
        return self._request.post(self.api_url + url, hooks=hooks, params=params, headers=headers)

    def r_upload(self, url, files, data=None, headers=None):
        hooks = dict(args=self.request_hook)
        upload_api_url = self.upload_api_url or self.api_url
        return self._request.post(upload_api_url + url, files=files, data=data, hooks=hooks)
