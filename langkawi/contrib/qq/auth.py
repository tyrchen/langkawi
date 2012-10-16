from django.contrib.sites.models import Site
from langkawi.contrib.qq.models import QQProfile
from django.contrib.auth.backends import ModelBackend
from langkawi.auth import LKWBackend


class QQAuth(LKWBackend):
    def authenticate(self, openid=None):
        try:
            return QQProfile.objects.get(
                openid=openid,
                site=Site.objects.get_current()).user
        except QQProfile.DoesNotExist:
            return None
