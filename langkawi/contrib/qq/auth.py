from django.contrib.sites.models import Site
from socialregistration.contrib.qq.models import QQProfile
from django.contrib.auth.backends import ModelBackend


class QQAuth(ModelBackend):
    def authenticate(self, qq=None):
        try:
            return QQProfile.objects.get(
                qq=qq,
                site=Site.objects.get_current()).user
        except QQProfile.DoesNotExist:
            return None
