#from django.db import models
#from django.contrib.auth.models import User
#from django.contrib.sites.models import Site


#class FriendsRelationship(models.Model):
#    user = models.ForeignKey(User, unique=False)
#    site = models.ForeignKey(Site, default=Site.objects.get_current)
#    friend_id = models.CharField(max_length=50)
#    third_part = models.CharField(max_length=20)
#    created_at = models.DateField(auto_now_add=True)

#   def __unicode__(self):
#        return u'%s has friend: %s in %s' % (self.user, self.friend_id, self.third_part)
