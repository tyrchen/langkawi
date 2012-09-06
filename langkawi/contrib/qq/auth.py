from django.contrib.sites.models import Site
from langkawi.contrib.qq.models import QQProfile
from django.contrib.auth.backends import ModelBackend


class QQAuth(ModelBackend):
    def authenticate(self, openid=None):
        try:
            return QQProfile.objects.get(
                open_id=openid,
                site=Site.objects.get_current()).user
        except QQProfile.DoesNotExist:
            return None
