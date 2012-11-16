from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from langkawi.signals import connect


class RenrenProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    site = models.ForeignKey(Site, default=Site.objects.get_current)
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=50,blank=True, default='')
    profile_image_url = models.URLField(blank=True, default='')

    class Meta:
        db_table = 'social_renrenprofile'

    def __unicode__(self):
        try:
            return u'%s: %s' % (self.user, self.uid)
        except User.DoesNotExist:
            return u'None'

    def authenticate(self):
        return authenticate(uid=self.uid)


class RenrenAccessToken(models.Model):
    profile = models.OneToOneField(RenrenProfile, related_name='access_token')
    access_token = models.CharField(max_length=255)
    token_expires_in = models.IntegerField()

    class Meta:
        db_table = 'social_renrenaccesstoken'


def save_renren_token(sender, user, profile, client, **kwargs):
    try:
        RenrenAccessToken.objects.get(profile=profile).delete()
    except RenrenAccessToken.DoesNotExist:
        pass

    RenrenAccessToken.objects.create(access_token=client.get_access_token(),
        profile=profile, token_expires_in=client.token_expires_in)


connect.connect(save_renren_token, sender=RenrenProfile,
    dispatch_uid='langkawi_renren_token')
