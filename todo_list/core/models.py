from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ocupation = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserData.objects.create(user=instance)
    instance.userdata.save()

class Card(models.Model):
    IMPORTANCE_OPTIONS = (
        (1, 'low'),
        (2, 'normal'),
        (3, 'urgent'),
    )
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=250, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    limit = models.DateTimeField(null=True, blank=True)

    finished = models.BooleanField(default=False)

    importance = models.IntegerField(choices=IMPORTANCE_OPTIONS, default=IMPORTANCE_OPTIONS[0][0])
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} | {}".format(self.author, self.name)
