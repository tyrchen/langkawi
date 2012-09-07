from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class QQProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    openid = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    profile_image_url = models.URLField()

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.openid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(openid=self.openid)


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
    dispatch_uid='langkawi_qq_token')
