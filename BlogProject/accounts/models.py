from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)


def save_profile(sender, **kwargs):
    if kwargs['created']:
        p = Profile(user=kwargs['instance'])
        p.save()


post_save.connect(save_profile, sender=User)
