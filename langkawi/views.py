from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from langkawi.clients.oauth import OAuthError
from langkawi.mixins import SocialRegistration

def initial_form_data(request, user, profile, client):
    initial_data = {}
    initial_data['username'] = profile.name
    if 'invite_email' in request.session:
        initial_data['email'] = request.session['invite_email']
    return initial_data

GENERATE_USERNAME = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME', False)

INVITE_MODE = getattr(settings, 'INVITE_MODE', False)

USERNAME_FUNCTION = getattr(settings, 'SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION',
    'langkawi.utils.generate_username')

FORM_CLASS = getattr(settings, 'SOCIALREGISTRATION_SETUP_FORM',
    'langkawi.forms.UserForm')

INITIAL_DATA_FUNCTION = getattr(settings, 'SOCIALREGISTRATION_INITIAL_DATA_FUNCTION',
    'langkawi.views.initial_form_data')



class Setup(SocialRegistration, View):
    """
    Setup view to create new Django users from third party APIs.
    """
    template_name = 'langkawi/setup.html'

    def get_form(self):
        """
        Return the form to be used. The return form is controlled
        with ``SOCIALREGISTRATION_SETUP_FORM``.
        """
        return self.import_attribute(FORM_CLASS)

    def get_username_function(self):
        """
        Return a function that can generate a username. The function
        is controlled with ``SOCIALREGISTRATION_GENERATE_USERNAME_FUNCTION``.
        """
        return self.import_attribute(USERNAME_FUNCTION)

    def get_initial_data(self, request, user, profile, client):
        """
        Return initial data for the setup form. The function can be
        controlled with ``SOCIALREGISTRATION_INITIAL_DATA_FUNCTION``.

        :param request: The current request object
        :param user: The unsaved user object
        :param profile: The unsaved profile object
        :param client: The API client
        """
        if INITIAL_DATA_FUNCTION:
            func = self.import_attribute(INITIAL_DATA_FUNCTION)
            return func(request, user, profile, client)
        return {}

    def generate_username_and_redirect(self, request, user, profile, client):
        """
        Generate a username and then redirect the user to the correct place.
        This method is called when ``SOCIALREGISTRATION_GENERATE_USERNAME``
        is set.

        :param request: The current request object
        :param user: The unsaved user object
        :param profile: The unsaved profile object
        :param client: The API client
        """
        func = self.get_username_function()

        user.username = func(user, profile, client)
        user.set_unusable_password()
        user.save()

        profile.user = user
        profile.save()

        user = profile.authenticate()

        request.user = user

        self.send_connect_signal(request, user, profile, client)

        self.login(request, user)

        self.send_login_signal(request, user, profile, client)

        self.delete_session_data(request)

        return HttpResponseRedirect(self.get_next(request))

    def get(self, request):
        """
        When signing a new user up - either display a setup form, or
        generate the username automatically.
        """
        try:
            user, profile, client = self.get_session_data(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("Social profile is missing from your session.")))

        if GENERATE_USERNAME:
            return self.generate_username_and_redirect(request, user, profile, client)
        form = self.get_form()(initial=self.get_initial_data(request, user, profile, client))

        return self.render_to_response(dict(form=form))

    def post(self, request):
        """
        Save the user and profile, login and send the right signals.
        """
        try:
            user, profile, client = self.get_session_data(request)
        except KeyError:
            return self.render_to_response(dict(
                error=_("A social profile is missing from your session.")))

        form = self.get_form()(request.POST, request.FILES,
            initial=self.get_initial_data(request, user, profile, client))

        if not form.is_valid():
            return self.render_to_response(dict(form=form))

        user, profile = form.save(request, user, profile, client)

        user = profile.authenticate()

        #client.create_friendships(user, profile)
        # Profile Status - Login status
        profile.status = 2
        profile.save()

        if not user.is_active:
            return self.inactive_response(request, user)

        self.send_connect_signal(request, user, profile, client)

        self.login(request, user)

        self.send_login_signal(request, user, profile, client)

        self.delete_session_data(request)

        return self.redirect(request)


class Logout(View):
    """
    Log the user out of Django. This **does not** log the user out
    of third party sites.
    """
    def get(self, request):
        logout(request)
        url = getattr(settings, 'LOGOUT_REDIRECT_URL', '/')
        return HttpResponseRedirect(url)


class OAuthRedirect(SocialRegistration, View):
    """
    Base class for both OAuth and OAuth2 redirects.

    :param client: The API client class that should be used.
    :param template_name: The error template.
    """

    # The OAuth{1,2} client to be used
    client = None

    # The template to render in case of errors
    template_name = None

    def post(self, request):
        """
        Create a client, store it in the user's session and redirect the user
        to the API provider to authorize our app and permissions.
        """
        request.session['customized'] = self.get_customized_response(request)
        request.session['next'] = self.get_next(request)

        client = self.get_client()()
        request.session[self.get_client().get_session_key()] = client
        try:
            return HttpResponseRedirect(client.get_redirect_url())
        except OAuthError, error:
            return self.render_to_response({'error': error})


class OAuthCallback(SocialRegistration, View):
    """
    Base class for OAuth and OAuth2 callback views.

    :param client: The API client class that should be used.
    :param template_name: The error template.
    """

    # The OAuth{1,2} client to be used
    client = None

    # The template to render in case of errors
    template_name = None

    def get_redirect(self):
        """
        Return a URL that will set up the correct models if the
        OAuth flow succeeded. Subclasses **must** override this
        method.
        """
        raise NotImplementedError

    def get(self, request):
        """
        Called after the user is redirected back to our application.
        Tries to:

        - Complete the OAuth / OAuth2 flow
        - Redirect the user to another view that deals with login, connecting
          or user creation.

        """
        try:
            client = request.session[self.get_client().get_session_key()]
            client.complete(dict(request.GET.items()))
            request.session[self.get_client().get_session_key()] = client
            return HttpResponseRedirect(self.get_redirect())
        except KeyError:
            return self.render_to_response({'error': "Session expired."})
        except OAuthError, error:
            return self.render_to_response({'error': error})


class SetupCallback(SocialRegistration, View):
    """
    Base class for OAuth and OAuth2 login / connects / registration.
    """

    def get(self, request):
        """
        Called after authorization was granted and the OAuth flow
        successfully completed.

        Tries to:

        - Connect the remote account if the user is logged in already
        - Log the user in if a local profile of the remote account
          exists already
        - Create a user and profile object if none of the above succeed
          and redirect the user further to either capture some data via
          form or generate a username automatically
        """
        try:
            client = request.session[self.get_client().get_session_key()]
        except KeyError:
            return self.render_to_response({'error': "Session expired..."})

        # Get the lookup dictionary to find the user's profile
        lookup_kwargs = self.get_lookup_kwargs(request, client)
        # Logged in user connecting an account
        if request.user.is_authenticated():
            profile, created = self.get_or_create_profile(request.user,
                save=True, **lookup_kwargs)
            # Profile Status - Binding an exist user
            if created:
                profile.status = 1
                profile.save()
            elif 'next' in request.session:
                request.session['next'] = request.session['next'] + "?ok=false&account=%s" % \
                    profile.user.email

            # Profile existed - but got reconnected. Send the signal and
            # send the 'em where they were about to go in the first place.
            self.send_connect_signal(request, request.user, profile, client)

            return self.redirect(request)

        # Logged out user - let's see if we've got the identity saved already.
        # If so - just log the user in. If not, create profile and redirect
        # to the setup views
        user = self.authenticate(**self.uid)
        # No user existing - create a new one and redirect to the final setup view
        if user is None:
            if INVITE_MODE and not 'invite_code' in request.session:
                return HttpResponseRedirect(reverse('invitation_invite'))

            user = self.create_user()
            profile = self.create_profile(user, **lookup_kwargs)
            self.store_user(request, user)
            self.store_profile(request, profile)
            self.store_client(request, client)
            return HttpResponseRedirect(reverse('langkawi:setup'))

        # Inactive user - displaying / redirect to the appropriate place.
        if not user.is_active:
            return self.inactive_response(request, user)

        # Active user with existing profile: login, send signal and redirect
        self.login(request, user)

        profile = self.get_profile(user=user, **lookup_kwargs)
        self.send_login_signal(request, user, profile, client)
        return self.redirect(request)

class UnbindingView(SocialRegistration, View):

    def post(self, request):
        if request.POST['unbind'] == '1' and request.user:
            status, code = self.unbind_profile(request.user)
            return HttpResponse(simplejson.dumps({'status':status, 'code':code}))
        else:
            return HttpResponse(simplejson.dumps({'status': False}))


