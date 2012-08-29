from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class RenrenProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    renren = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.renren)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(renren=self.renren)


class RenrenAccessToken(models.Model):
    profile = models.OneToOneField(RenrenProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)


def save_renren_token(sender, user, profile, client, **kwargs):
    try:
        RenrenAccessToken.objects.get(profile=profile).delete()
    except RenrenAccessToken.DoesNotExist:
        pass

    RenrenAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile)


connect.connect(save_renren_token, sender=RenrenProfile,
    dispatch_uid='langkawi_renren_token')
