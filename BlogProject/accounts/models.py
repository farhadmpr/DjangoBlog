from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    mobile = models.PositiveIntegerField(null=True, blank=True)


def save_profile(sender, **kwargs):
    if kwargs['created']:
        p = Profile(user=kwargs['instance'])
        p.save()


# signal
post_save.connect(save_profile, sender=User)



class UserRelation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return f'{self.from_user} follow {self.to_user}'

    