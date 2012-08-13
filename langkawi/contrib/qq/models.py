from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class QQProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    qq = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.qq)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(qq=self.qq)


class QQAccessToken(models.Model):
    profile = models.OneToOneField(QQProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)


def save_qq_token(sender, user, profile, client, **kwargs):
    try:
        QQAccessToken.objects.get(profile=profile).delete()
    except QQAccessToken.DoesNotExist:
        pass

    QQAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile)


connect.connect(save_qq_token, sender=QQProfile,
    dispatch_uid='socialregistration_qq_token')
